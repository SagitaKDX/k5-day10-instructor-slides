// Encrypt the Day 10 card pack once, then add download codes room by room.
//
//   node tools/card-pack/build_pack.mjs init <the-su-co-day10.zip> <public-dir> <secret-dir>
//   node tools/card-pack/build_pack.mjs add  <room> <count> <public-dir> <secret-dir>
//
// init: encrypts the zip with a new random AES-256-GCM key K, writes <public-dir>/pack.enc and an
//       empty <public-dir>/keys.json, and saves K to <secret-dir>/master.key. Every older code stops working.
// add:  reads K from <secret-dir>/master.key, makes <count> new codes for <room>, adds their entries
//       to keys.json and writes <secret-dir>/codes-<room>.csv. Older codes keep working.
//
// Public files (pack.enc, keys.json) are safe on GitHub Pages. master.key and codes-*.csv are secret.
//
// Design
// - Each code is XXXX-XXXX-XXXX from a 32-letter alphabet (5 bits per letter, no 0/O or 1/I).
//   The first 4 letters are a public lookup id; the last 8 letters (40 bits) are secret.
// - For each code, K is wrapped with AES-GCM under a key from PBKDF2-SHA256(code, salt, ITER).
//   Guessing one code offline costs 2^40 PBKDF2 runs.
// - All tables get the same pack (all 8 cards): lab10.grade checks the hashes of all 32 card files.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs'
import { join } from 'node:path'

const ITER = 300000
const ALPHA = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
const { subtle } = globalThis.crypto
const b64 = (u8) => Buffer.from(u8).toString('base64')
const die = (m) => { console.error(m); process.exit(2) }

function randomCode() {
  const bytes = crypto.getRandomValues(new Uint8Array(12))
  const s = Array.from(bytes, (b) => ALPHA[b & 31]).join('')
  return `${s.slice(0, 4)}-${s.slice(4, 8)}-${s.slice(8, 12)}`
}
async function kekFor(code, salt) {
  const base = await subtle.importKey('raw', new TextEncoder().encode(code.replace(/-/g, '')), 'PBKDF2', false, ['deriveKey'])
  return subtle.deriveKey({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations: ITER }, base,
    { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt'])
}

const [cmd, ...a] = process.argv.slice(2)

if (cmd === 'init') {
  const [zipPath, pubDir, secretDir] = a
  if (!zipPath || !pubDir || !secretDir) die('usage: build_pack.mjs init <zip> <public-dir> <secret-dir>')
  const zip = readFileSync(zipPath)
  const rawK = crypto.getRandomValues(new Uint8Array(32))
  const K = await subtle.importKey('raw', rawK, 'AES-GCM', false, ['encrypt'])
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const ct = new Uint8Array(await subtle.encrypt({ name: 'AES-GCM', iv }, K, zip))
  mkdirSync(pubDir, { recursive: true }); mkdirSync(secretDir, { recursive: true })
  writeFileSync(join(pubDir, 'pack.enc'), Buffer.concat([Buffer.from(iv), Buffer.from(ct)]))
  writeFileSync(join(pubDir, 'keys.json'), JSON.stringify({ v: 1, kdf: 'PBKDF2-SHA256', iter: ITER, zip: 'the-su-co-day10.zip', size: zip.length, entries: {} }))
  writeFileSync(join(secretDir, 'master.key'), Buffer.from(rawK).toString('base64') + '\n', { mode: 0o600 })
  console.log(`init: pack ${zip.length} B -> pack.enc; keys.json empty; master.key saved. Older codes no longer work.`)
} else if (cmd === 'add') {
  const [room, countArg, pubDir, secretDir] = a
  const count = Number(countArg)
  if (!room || !/^[A-Za-z0-9_-]+$/.test(room) || !Number.isInteger(count) || count < 1 || !pubDir || !secretDir)
    die('usage: build_pack.mjs add <room, letters/digits only> <count> <public-dir> <secret-dir>')
  const keyPath = join(secretDir, 'master.key')
  if (!existsSync(keyPath)) die(`no ${keyPath}: run init first`)
  const rawK = Buffer.from(readFileSync(keyPath, 'utf8').trim(), 'base64')
  const keysPath = join(pubDir, 'keys.json')
  const keys = JSON.parse(readFileSync(keysPath, 'utf8'))
  const outPath = join(secretDir, `codes-${room}.csv`)
  const rows = existsSync(outPath) ? readFileSync(outPath, 'utf8').trimEnd().split('\n') : ['stt,ma']
  let n = rows.length - 1
  for (let i = 0; i < count; i++) {
    let code
    do { code = randomCode() } while (keys.entries[code.slice(0, 4)])
    const salt = crypto.getRandomValues(new Uint8Array(16))
    const iv = crypto.getRandomValues(new Uint8Array(12))
    const wrapped = new Uint8Array(await subtle.encrypt({ name: 'AES-GCM', iv }, await kekFor(code, salt), rawK))
    keys.entries[code.slice(0, 4)] = { s: b64(salt), i: b64(iv), w: b64(wrapped) }
    rows.push(`${++n},${code}`)
  }
  writeFileSync(keysPath, JSON.stringify(keys))
  writeFileSync(outPath, rows.join('\n') + '\n')
  console.log(`add: ${count} codes for ${room} -> ${outPath} (${n} in the file); keys.json now has ${Object.keys(keys.entries).length} codes`)
} else {
  die('usage: build_pack.mjs init <zip> <public-dir> <secret-dir> | add <room> <count> <public-dir> <secret-dir>')
}
