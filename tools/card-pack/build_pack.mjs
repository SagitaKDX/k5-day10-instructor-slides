// Encrypt the Day 10 card pack and make one download code per table.
//
//   node tools/card-pack/build_pack.mjs <the-su-co-day10.zip> <public-out-dir> <secret-out-dir> [clusters=10] [per-cluster=16]
//
// Public output (safe to publish on GitHub Pages):  pack.enc, keys.json
// Secret output (coach only, never commit):         codes-cum-01.csv … codes-cum-NN.csv, codes-all.csv
//
// Design
// - The zip is encrypted once with a random AES-256-GCM key K.
// - Each code is XXXX-XXXX-XXXX from a 32-letter alphabet (5 bits per letter).
//   The first 4 letters are a public lookup id. The last 8 letters (40 bits) are secret.
// - For each code, K is wrapped with AES-GCM under a key from PBKDF2-SHA256(code, salt, ITER).
//   Without a valid code, nobody can get K. Guessing one code offline costs 2^40 PBKDF2 runs.
// - All tables get the same pack (all 8 cards): lab10.grade checks the hashes of all 32 card files.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join } from 'node:path'

const [zipPath, pubDir, secretDir, clustersArg = '10', perArg = '16'] = process.argv.slice(2)
if (!zipPath || !pubDir || !secretDir) {
  console.error('usage: node build_pack.mjs <zip> <public-out-dir> <secret-out-dir> [clusters] [per-cluster]')
  process.exit(2)
}
const CLUSTERS = Number(clustersArg)
const PER = Number(perArg)
const ITER = 300000
const ALPHA = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ' // no 0/O, 1/I
const { subtle } = globalThis.crypto
const b64 = (u8) => Buffer.from(u8).toString('base64')

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

const zip = readFileSync(zipPath)
const rawK = crypto.getRandomValues(new Uint8Array(32))
const K = await subtle.importKey('raw', rawK, 'AES-GCM', false, ['encrypt'])
const packIv = crypto.getRandomValues(new Uint8Array(12))
const packCt = new Uint8Array(await subtle.encrypt({ name: 'AES-GCM', iv: packIv }, K, zip))
mkdirSync(pubDir, { recursive: true })
mkdirSync(secretDir, { recursive: true })
writeFileSync(join(pubDir, 'pack.enc'), Buffer.concat([Buffer.from(packIv), Buffer.from(packCt)]))

const entries = {}
const all = ['cum,stt,ma']
for (let c = 1; c <= CLUSTERS; c++) {
  const rows = ['stt,ma']
  for (let i = 1; i <= PER; i++) {
    let code
    do { code = randomCode() } while (entries[code.slice(0, 4)])
    const salt = crypto.getRandomValues(new Uint8Array(16))
    const iv = crypto.getRandomValues(new Uint8Array(12))
    const wrapped = new Uint8Array(await subtle.encrypt({ name: 'AES-GCM', iv }, await kekFor(code, salt), rawK))
    entries[code.slice(0, 4)] = { s: b64(salt), i: b64(iv), w: b64(wrapped) }
    rows.push(`${i},${code}`)
    all.push(`${c},${i},${code}`)
  }
  writeFileSync(join(secretDir, `codes-cum-${String(c).padStart(2, '0')}.csv`), rows.join('\n') + '\n')
}
writeFileSync(join(secretDir, 'codes-all.csv'), all.join('\n') + '\n')
writeFileSync(join(pubDir, 'keys.json'), JSON.stringify({ v: 1, kdf: 'PBKDF2-SHA256', iter: ITER, zip: 'the-su-co-day10.zip', size: zip.length, entries }))
console.log(`pack ${zip.length} B -> pack.enc; ${CLUSTERS} x ${PER} = ${CLUSTERS * PER} codes`)
