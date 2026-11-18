"""Builds app/src/slides/content.json for the Day 10 instructor deck.

Same frame as the Day 02 / Day 03 decks: opening, format, goals, schedule, naming, rules, one slide
per checkpoint (meta bar, task, coach, anti-pattern, self-check), phase transitions, rubric, and the
submission checklist.

Facts come from the Day 10 lab repo (VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student, branch
docs/k5-lab-convention, PR #1): README.md, problem-set.md, CHECKPOINTS.md, RULES.md, RUBRIC.md,
SUBMISSION.md, TEAM.md, submission/README.md, incidents/README.md, docs/guide.md.
The lab counts minutes 0 to 240; the deck writes them as afternoon clock times (minute 0 = 13:30)
and the app shifts them for the morning class (app/src/session.ts).

Run from the repo root:  python3 -I content/build_content.py
"""
import json
import pathlib
import re

ICONS = json.loads((pathlib.Path(__file__).resolve().parent / "icons.json").read_text())

S = []
_PENDING_NOTES = []


def slide(title, html, notes, cp=None, minutes=None, label=None, done=None):
    if _PENDING_NOTES:
        extra = "".join(f"<li>{x}</li>" for x in _PENDING_NOTES)
        notes = notes.strip() + f"\n<strong>Coach nói (chi tiết)</strong>\n<ul>{extra}</ul>"
        _PENDING_NOTES.clear()
    S.append({
        "index": len(S),
        "title": title,
        "html": html.strip().replace("{ICONS_ANTI}", ICONS["anti"]),
        "notes": notes.strip(),
        "activeCp": cp,
        "timerMin": minutes,
        "timerLabel": label,
        "completedThrough": done,
    })


def meta(**rows):
    names = {
        "time": "Thời lượng",
        "when": "Giờ",
        "who": "Ai làm",
        "write": "Ghi vào",
        "out": "Sản phẩm",
        "bonus": "Điểm thưởng",
    }
    body = "".join(f"<div><dt>{names[k]}</dt><dd>{v}</dd></div>" for k, v in rows.items())
    return f'<dl class="meta">{body}</dl>'


def coach(*items):
    """Slide shows the bold lead of each item; the full sentence goes to the speaker notes."""
    shown = []
    for x in items:
        m = re.match(r"<b>(.*?)</b>(.*)", x, re.S)
        if m and m.group(2).strip():
            shown.append(m.group(1).rstrip(":").rstrip())
            _PENDING_NOTES.append(x)
        else:
            shown.append(x)
    li = "".join(f"<li>{x}</li>" for x in shown)
    return f'<section class="coach"><h3>{ICONS["coach"]}Coach nói</h3><ul>{li}</ul></section>'


def anti(*items):
    li = "".join(f"<li>{x}</li>" for x in items)
    return f'<section class="anti"><h3>{ICONS["anti"]}Lỗi thường gặp</h3><ul>{li}</ul></section>'


def check(text):
    return f'<section class="selfcheck"><h3>{ICONS["check"]}Tự kiểm tra</h3><p>{text}</p></section>'


# Writing rules for this deck (ASD-STE100 applied to Vietnamese):
# - One sentence = one idea. Procedure sentences: at most 20 words. Description sentences: at most 25 words.
# - An instruction starts with the verb ("Chạy …", "Ghi …"). Active voice. No idioms, no figurative words.
# - One word = one meaning. Use the term list on slide 2 ("Từ dùng trong buổi") and no synonyms:
#   bàn, cổng, tiêu chí, lần chạy, mốc, thẻ sự cố, người phụ trách, quyết định.
# - Use a list when there are more than two items. Keep code, commands, paths, times and numbers unchanged.

# 0 ── Title ─────────────────────────────────────────────────────────────
slide(
    "Day 10: From PoC to Pilot (Gate 1)",
    """
<div class="title-slide">
  <div class="title-copy">
    <p class="course"><b>Day 10 · From PoC to Pilot (Gate 1)</b> · VinUni AI20k, K5 Level 3 (3A và 3B), {{SESSION}}, {{SESSION_RANGE}}</p>
    <h1 class="hero">Ký tiêu chí trước. Đo sau. Quyết định theo số đo.</h1>
    <p class="lede">LogiX-VN có một trợ lý AI hoàn tiền khi giao hàng trễ. Bàn quyết định: cho trợ lý chạy thử với khách thật ở 2 kho, hay chưa.</p>
  </div>
  <figure class="title-proof">
    <figcaption>Cuối buổi, bàn chiếu ba mốc đo này:</figcaption>
<pre class="code code--big"><span class="c"># python3 -m lab10.grade --incident Sx</span>
            base   prepared   after
cổng của bàn  —     vòng 1    vòng 2
quyết định    —       v1        v2
<span class="c"># Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng</span></pre>
  </figure>
</div>
<div class="facts">
  <section><h2>Hình thức</h2><p>Làm theo bàn, 4–5 người. 240 phút.</p></section>
  <section><h2>Chấm điểm</h2><p>Không chấm tại lớp. Team chấm chấm sau buổi: 100 điểm, thêm tối đa 10 điểm thưởng.</p></section>
  <section><h2>Hạn nộp</h2><p>{{DEADLINE}} (GMT+7).</p></section>
  <section><h2>Phím</h2><p><kbd>←</kbd> <kbd>→</kbd>: đổi slide. <kbd>N</kbd>: ghi chú.</p></section>
</div>
""",
    """
<strong>Mở đầu buổi học</strong>
<ul>
  <li>Nói với lớp: hôm nay không đo “trợ lý trả lời hay không”.</li>
  <li>Câu hỏi của buổi: có đủ số đo để cho trợ lý chạy thử với khách thật không?</li>
  <li>Bàn cũng phải trả lời: tốn bao nhiêu tiền, cần mấy người trực, ai chịu trách nhiệm.</li>
  <li>Có bốn quyết định: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng. Quyết định nào cũng đạt nếu khớp số đo và khớp tiêu chí đã ký.</li>
  <li>Không ai chấm điểm tại lớp. Các lệnh chỉ để bàn tự kiểm tra.</li>
  <li>Team chấm đọc repo của bàn sau buổi học. Team chấm chạy thêm bộ test ẩn.</li>
  <li>Trợ lý dùng MockLLM. Mỗi lần chạy cho cùng một kết quả. Bàn không cần API key.</li>
</ul>
""",
)

# 0b ── Context ─────────────────────────────────────────────────────────
slide(
    "Bối cảnh: trợ lý của LogiX-VN",
    """
<h2 class="title">Bối cảnh: trợ lý hoàn tiền của LogiX-VN</h2>
<p class="lede">Khách nhắn khiếu nại về giao hàng. Trợ lý AI đọc tin nhắn, tra đơn, rồi tự làm 4 việc.</p>
<div class="grid grid-2">
  <section class="panel">
    <h3>4 việc trợ lý tự làm</h3>
    <ul class="plain">
      <li><code>issue_refund</code>: hoàn tiền cho khách.</li>
      <li><code>file_carrier_fault</code>: ghi lỗi cho hãng vận chuyển.</li>
      <li><code>notify_carrier</code>: báo cho hãng.</li>
      <li><code>send_reply</code>: trả lời khách.</li>
    </ul>
    <p class="cp-ref">Mỗi việc làm sai đều gây thiệt hại: mất tiền, ghi lỗi oan cho hãng, lộ dữ liệu khách.</p>
  </section>
  <section class="panel">
    <h3>Ví dụ: ticket <code>T-002</code></h3>
    <p>Khách viết: “Đơn giao trễ 5 ngày rồi, tôi muốn được hoàn phí vận chuyển.”</p>
    <p>Đáp án đúng: không hoàn tiền. Trợ lý cũng có thể chuyển ca này cho người duyệt.</p>
    <p class="cp-ref">Ở CP3, bàn chạy trace ticket này để xem trợ lý làm gì.</p>
  </section>
</div>
<section class="panel panel--do">
  <h3>Câu hỏi Gate 1: cho trợ lý chạy thử với khách thật không?</h3>
  <p>Bàn chọn một trong bốn: <b>Tiếp tục</b> (chạy pilot) · <b>Thu hẹp</b> (chạy ở phạm vi nhỏ hơn) · <b>Cải tiến thêm</b> (sửa rồi đánh giá lại) · <b>Dừng</b>.</p>
</section>
""",
    """
<strong>Cách mở bài</strong>
<ul>
  <li>Đọc to tin nhắn của ticket <code>T-002</code>. Hỏi lớp: “Trợ lý có nên hoàn tiền không?”</li>
  <li>Nói: trợ lý không chỉ trả lời. Trợ lý tự ghi tiền và ghi lỗi. Vì vậy, một lỗi nhỏ gây thiệt hại thật.</li>
  <li>Nói: hôm nay bàn không sửa trợ lý cho “đúng hết”. Bàn quyết định có cho trợ lý chạy thật hay không, kèm bằng chứng.</li>
  <li>Dữ liệu trong <code>data/world.json</code> là dữ liệu giả, nhưng có số thật về người trực, chi phí và trần tiền.</li>
</ul>
""",
)

# 1 ── Format ────────────────────────────────────────────────────────────
slide(
    "Hình thức: một bàn, ba vai, hai vòng",
    """
<h2 class="title">Một bàn, ba vai, hai vòng</h2>
<p class="lede">Ở vòng 1, bàn chưa biết sự cố. Ở vòng 2, bàn nhận thẻ sự cố và đo cổng của vòng 1.</p>
<div class="grid grid-3 roles">
  <section class="panel"><h3>Kỹ sư cổng (1–2 người)</h3><p>Chạy lệnh và trace. Viết cổng trong <code>lab10/guards.py</code>. Viết chỉ số theo dõi trong <code>lab10/monitors.py</code>.</p></section>
  <section class="panel"><h3>Sản phẩm và kinh doanh (1–2 người)</h3><p>Viết tiêu chí. Đặt cổng <code>business</code>. Đọc chi phí và ROI. Viết quyết định v1 và v2.</p></section>
  <section class="panel"><h3>Vận hành và pháp lý (1 người)</h3><p>Viết HAZOP và checklist 9 nhóm việc. Đặt cổng <code>operations</code> và <code>legal</code>. Viết runbook. Gom bài nộp.</p></section>
</div>
<ol class="loop loop--three">
  <li><b>Vòng 1 · 13:45–15:25</b><span>Ký tiêu chí. Đo. Tìm rủi ro. Viết cổng. Chốt v1.</span></li>
  <li><b>Phát thẻ · 15:35</b><span>Mỗi cặp bàn bốc một thẻ, S1–S8.</span></li>
  <li><b>Vòng 2 · 15:35–16:50</b><span>Đo lại. Tìm nguyên nhân. Sửa. Quyết định v2.</span></li>
</ol>
""",
    """
<strong>Cách bàn làm việc</strong>
<ul>
  <li>Người không viết code cũng có việc: tiêu chí, chi phí, số người trực, runbook, quyết định.</li>
  <li>Bàn chỉ sửa các file trong README mục 1.</li>
  <li>Các file khác có khóa hash. Nếu bàn sửa, lệnh tự kiểm tra báo lỗi.</li>
  <li>Bảng thành viên nằm trong <code>TEAM.md</code>, không nằm trong README.</li>
  <li>Mỗi người viết mục <code>## HoVaTen-MSSV</code> của mình. Mục này có cả exit ticket.</li>
</ul>
""",
)

# 1b ── Flow ────────────────────────────────────────────────────────────
slide(
    "Cả buổi trên một trang",
    """
<h2 class="title">Cả buổi trên một trang</h2>
<h3 class="sub">Vòng 1 · bàn chưa biết sự cố</h3>
<ol class="loop loop--flow">
  <li><b>Ký tiêu chí</b><span>13:45–14:35 · lệnh 1. Ký trước khi đo.</span></li>
  <li><b>Đo base</b><span>14:35 · lệnh 2, 3, 4. Trợ lý chưa có cổng.</span></li>
  <li><b>Tìm rủi ro</b><span>14:35–14:55 · HAZOP, checklist, pre-mortem.</span></li>
  <li><b>Viết cổng</b><span>14:55–15:15 · <code>guards.py</code>, <code>operating_gates.json</code>.</span></li>
  <li><b>Chốt và v1</b><span>15:15–15:25 · lệnh 5. Đo prepared. Viết v1.</span></li>
</ol>
<h3 class="sub">Vòng 2 · bàn có thẻ sự cố</h3>
<ol class="loop loop--flow" style="counter-reset: step 5">
  <li><b>Nhận thẻ</b><span>15:35 · kéo thẻ từ <code>upstream</code>. Bốc S1–S8.</span></li>
  <li><b>Đo ngay</b><span>15:35–15:45 · lệnh 6. Chưa sửa gì.</span></li>
  <li><b>Tìm nguyên nhân và sửa</b><span>15:45–16:35 · trace, fault tree, sửa, thêm chỉ số theo dõi.</span></li>
  <li><b>v2 và gom bài</b><span>16:35–16:50 · Phiếu C mục C12. Lệnh 7.</span></li>
  <li><b>Demo và nộp</b><span>16:50–17:30 · chiếu ba mốc. Push. Nộp LMS.</span></li>
</ol>
""",
    """
<strong>Ba chỗ bị khóa và lý do</strong>
<ul>
  <li>Bước 1, ký tiêu chí: bàn viết ngưỡng khi chưa biết kết quả. Nếu bàn xem kết quả trước, bàn dễ đặt ngưỡng vừa khớp kết quả.</li>
  <li>Bước 5, chốt vòng 1: lệnh 5 lưu một bản cổng. Ở vòng 2, lab so bản này với bản sửa. Nếu bàn sửa được bản chốt, phép so không còn ý nghĩa.</li>
  <li>Bước 7, đo ngay khi nhận thẻ: lần đo này là mốc prepared. Nếu bàn sửa trước, bàn mất mốc này.</li>
  <li>Nói với lớp: ba chỗ này có hash hoặc có giờ trong <code>runs/journal.jsonl</code>. Team chấm kiểm được thứ tự.</li>
</ul>
""",
)

# 2 ── Terms ─────────────────────────────────────────────────────────────
slide(
    "Từ dùng trong buổi",
    """
<h2 class="title">Từ dùng trong buổi: một từ, một nghĩa</h2>
<table class="data data--compact">
  <thead><tr><th>Từ</th><th>Nghĩa trong lab này</th></tr></thead>
  <tbody>
    <tr><td class="num">Gate 1</td><td>Bước đánh giá 1: cho trợ lý chạy thử với khách thật, hay chưa.</td></tr>
    <tr><td class="num">Bàn</td><td>Nhóm 4–5 người làm chung một repo.</td></tr>
    <tr><td class="num">Tiêu chí</td><td>Các ngưỡng đạt. Bàn ký tiêu chí một lần, trước khi đo.</td></tr>
    <tr><td class="num">Cổng</td><td>Một kiểm tra chặn hoặc giới hạn hành động của trợ lý. Cổng là code, con số trong config, hoặc người.</td></tr>
    <tr><td class="num">Lần chạy</td><td>Một lần chạy trợ lý trên một bộ ticket. Mỗi lần chạy có một mã.</td></tr>
    <tr><td class="num">Mốc</td><td>Ba cách đo: <code>base</code>, <code>prepared</code>, <code>after</code>.</td></tr>
    <tr><td class="num">Thẻ sự cố</td><td>Một tác hại cụ thể, S1–S8. Bàn nhận lúc 15:35.</td></tr>
    <tr><td class="num">Người phụ trách</td><td>Người có tên, chịu trách nhiệm một việc (PIC).</td></tr>
  </tbody>
</table>
""",
    """
<strong>Vì sao có slide này</strong>
<ul>
  <li>Cả buổi chỉ dùng các từ trong bảng, với đúng một nghĩa.</li>
  <li>Khi bàn dùng từ khác, hỏi lại: “Ý bạn là cổng hay tiêu chí?”</li>
  <li>“Tiêu chí” là ngưỡng bàn hứa. “Cổng” là cách bàn giữ ngưỡng đó.</li>
</ul>
""",
)

# 3 ── Goals ─────────────────────────────────────────────────────────────
slide(
    "Bốn mục tiêu học tập của Lab Day 10",
    """
<h2 class="title">Bốn mục tiêu học tập của Lab Day 10</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>Viết tiêu chí trước khi đo</h3>
    <p>Viết mỗi ngưỡng thành câu “Nếu … thì chúng tôi sẽ …”. Ký và push trước lần chạy đầu tiên.</p>
    <p class="cp-ref">CP2, tiêu chí chấm C1</p>
  </section>
  <section class="panel">
    <h3>Tìm rủi ro trước khi có sự cố</h3>
    <p>Làm pre-mortem bốn lăng kính. Làm HAZOP có dòng ngoài kỹ thuật. Ghi người phụ trách cho từng việc.</p>
    <p class="cp-ref">CP3, tiêu chí chấm C2</p>
  </section>
  <section class="panel">
    <h3>Đặt cổng bên ngoài model</h3>
    <p>Dùng code, con số trong config và người. Giữ đúng các ca đang đúng.</p>
    <p class="cp-ref">CP3, CP4, tiêu chí chấm C3, C4, C5</p>
  </section>
  <section class="panel">
    <h3>Quyết định theo số đo</h3>
    <p>Dùng report ba mốc và tiêu chí đã ký. Viết thêm ba dòng bắt buộc.</p>
    <p class="cp-ref">CP5, tiêu chí chấm C6</p>
  </section>
</div>
""",
    """
<strong>Liên hệ với RUBRIC.md (bản đề xuất trong PR #1)</strong>
<ul>
  <li>Mục tiêu 1 là điều kiện qua. Bàn ký sau khi đo, hoặc sửa sau khi ký: bài không được tính.</li>
  <li>Team chấm so lịch sử git với <code>runs/journal.jsonl</code>.</li>
  <li>Mục tiêu 3: chặn hết, thu hẹp về 0, hay xếp thật nhiều người trực đều không phải cách sửa.</li>
  <li>Report đo cả độ phủ, chi phí và ROI.</li>
  <li>Mục tiêu 4: report còn vượt trần mà bàn chọn Tiếp tục, thì quyết định không đạt.</li>
</ul>
""",
)

# 4 ── Schedule ──────────────────────────────────────────────────────────
slide(
    "Năm checkpoint và mốc giờ",
    """
<h2 class="title">Năm checkpoint và giờ bắt đầu</h2>
<table class="data">
  <thead><tr><th>Giờ</th><th>Checkpoint</th><th>Repo phải có</th><th>Phiếu</th></tr></thead>
  <tbody>
    <tr><td class="num">13:30</td><td><b>CP1</b> Cài đặt, chia vai</td><td><code>Ran 13 tests … OK</code>, <code>origin</code> và <code>upstream</code>, <code>TEAM.md</code></td><td>TEAM</td></tr>
    <tr class="row-key"><td class="num">13:45</td><td><b>CP2</b> Viết tiêu chí. Ký lúc 14:30–14:35</td><td><code>acceptance_criteria.json</code> và <code>.lock</code> đã push</td><td>A</td></tr>
    <tr><td class="num">14:35</td><td><b>CP3</b> Đo, tìm rủi ro, cổng vòng 1, v1</td><td>Mã lần chạy base, bản chốt vòng 1, v1 đã push</td><td>B</td></tr>
    <tr><td class="num">15:35</td><td><b>CP4</b> Thẻ sự cố S1–S8</td><td>Report ba mốc, <code>monitor ✅</code>, <code>regression ✅</code></td><td>C</td></tr>
    <tr><td class="num">16:35</td><td><b>CP5</b> v2, demo, nộp</td><td>Lệnh 7 in <code>ĐỦ THÀNH PHẦN</code></td><td>C12</td></tr>
  </tbody>
</table>
<p class="note">Nghỉ: 15:25–15:35. Push lần cuối: trước 17:30. Hạn nộp link LMS: {{DEADLINE}}.</p>
""",
    """
<strong>Giờ trong buổi</strong>
<ul>
  <li>Lab ghi giờ theo phút 0–240. Deck đổi sang giờ lớp chiều: phút 0 là 13:30.</li>
  <li>Lớp sáng dùng cùng lịch, sớm hơn 5 tiếng. Deck tự chọn ca theo giờ máy khi mở. Nút trên header đổi ca bằng tay.</li>
  <li>Mốc quan trọng nhất: ký tiêu chí lúc 14:30–14:35, trước lần chạy đầu tiên.</li>
  <li>Nếu bàn chạy <code>eval</code> trước khi ký, lệnh từ chối chạy.</li>
  <li>Nếu bàn ký mà không push ngay, lịch sử git không chứng minh được thứ tự.</li>
  <li>Mốc quan trọng thứ hai: chốt cổng vòng 1 (lệnh 5) lúc 15:15–15:25. Nếu không chốt, bàn không có mốc prepared.</li>
  <li>Lúc 15:35, coach đẩy thẻ lên repo mẫu. Bàn kéo thẻ bằng <code>git pull … upstream main</code>.</li>
</ul>
""",
)

# 5 ── Repo naming ───────────────────────────────────────────────────────
slide(
    "Tạo repo của bàn và đặt tên",
    """
<h2 class="title">Tạo repo của bàn. Đặt tên đúng từ đầu.</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>Tên repo của bàn</h3>
<pre class="code code--wrap">K5-L3A-DAY10-TenNhom-PoCtoPilotGate1
K5-L3B-DAY10-TenNhom-PoCtoPilotGate1</pre>
    <p>Viết <code>TenNhom</code> không dấu, không khoảng trắng. Không thêm chữ <code>Lop</code>.</p>
    <p>Ghi tên repo y hệt vào <code>team</code> của tiêu chí và của <code>submission.json</code>.</p>
    <h3>Gắn repo mẫu</h3>
<pre class="code code--wrap">git remote add upstream https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student.git
git remote -v</pre>
  </section>
  <div class="stack">
    <section class="panel">
      <h3>Tên người commit</h3>
<pre class="code">git config user.name "&lt;MSSV trưởng nhóm&gt;"
git config user.email "&lt;MSSV&gt;@example.com"</pre>
      <p>Để repo ở chế độ Private, dùng <b>Use this template</b>. Không dùng Fork.</p>
    </section>
    <section class="anti">
      <h3>{ICONS_ANTI}Lỗi thường gặp</h3>
      <ul>
        <li>Không mời tài khoản team chấm (quyền Read).</li>
        <li>Không gắn <code>upstream</code>. Lúc 15:35 bàn không kéo được thẻ.</li>
        <li>Push vào repo mẫu.</li>
      </ul>
    </section>
  </div>
</div>
""",
    """
<strong>Việc của coach trong 15 phút đầu</strong>
<ul>
  <li>Quy tắc tên lấy từ SUBMISSION.md của lab.</li>
  <li>Dạng tên: <code>Kn-L3{A|B}-DAYxx-TenNhom-TenBai</code>. Với lab này, <code>TenBai</code> là <code>PoCtoPilotGate1</code>.</li>
  <li>Dùng <code>L3A</code> cho lớp 3A và <code>L3B</code> cho lớp 3B. Viết <code>DAY10</code> bằng chữ hoa.</li>
  <li>Trưởng nhóm mở Settings → Collaborators. Trưởng nhóm mời tài khoản team chấm và các bạn trong bàn.</li>
  <li>Hỏi Lab Coach để biết tên tài khoản team chấm.</li>
  <li>Email Git là địa chỉ giả <code>&lt;MSSV&gt;@example.com</code>. Không dùng email cá nhân.</li>
  <li>Kiểm <code>git remote -v</code> của từng bàn. Phải có <code>origin</code> (repo của bàn) và <code>upstream</code> (repo mẫu).</li>
</ul>
""",
)

# 6 ── Rules ─────────────────────────────────────────────────────────────
slide(
    "Luật làm bài",
    """
<h2 class="title">Luật làm bài: làm gì, không làm gì</h2>
<table class="data">
  <thead><tr><th>Phần</th><th>Làm</th><th>Không làm</th></tr></thead>
  <tbody>
    <tr><td class="num">Tiêu chí</td><td>Ký một lần. Commit và push ngay.</td><td>Chạy <code>eval</code> trước khi ký. Sửa sau khi ký.</td></tr>
    <tr><td class="num">Bản chốt</td><td>Ở vòng 2, sửa <code>guards.py</code> và config gốc.</td><td>Sửa <code>guards_round1.py</code>, <code>*.round1.json</code>, <code>round1.lock</code>.</td></tr>
    <tr><td class="num">Test ẩn</td><td>Viết cổng theo quy tắc chung.</td><td>Viết cổng cho một mã ticket hay một câu chữ.</td></tr>
    <tr><td class="num">Ca đang đúng</td><td>Giữ ca đó đúng sau khi sửa.</td><td>Chặn hết. Thu hẹp về 0. Xếp quá nhiều người.</td></tr>
    <tr><td class="num">Thẻ sự cố</td><td>Làm thẻ của bàn.</td><td>Mở hoặc kể thẻ của bàn khác.</td></tr>
    <tr><td class="num">AI</td><td>Dùng AI để đọc code, gợi ý cổng, sửa câu.</td><td>Ghi con số mà bàn không giải thích được.</td></tr>
  </tbody>
</table>
<p class="note">Các file có khóa hash. Nếu bàn sửa, report báo <code>integrity</code> hỏng.</p>
""",
    """
<strong>Nói rõ với lớp (README mục 5 và RULES.md)</strong>
<ul>
  <li>Không mở rồi lưu lại <code>config/acceptance_criteria.json</code> bằng trình soạn thảo tự định dạng.</li>
  <li>Một dấu cách thêm vào cũng làm đổi hash.</li>
  <li>Lệnh 5 tạo ba file bản chốt vòng 1. Trước 15:15, ba file này chưa có. Đó là đúng.</li>
  <li>Các ngưỡng, con số trong <code>operating_gates.json</code> và quyết định là của bàn.</li>
  <li>AI được gợi ý. Bàn phải giải thích được khi bàn khác hỏi.</li>
  <li>Không commit API key, mật khẩu, file <code>.env</code>. Lab không cần key.</li>
</ul>
""",
)

# 7 ── CP1 ───────────────────────────────────────────────────────────────
slide(
    "CP1: Cài đặt và chia vai",
    f"""
<h2 class="title">CP1: chạy được repo, chia vai</h2>
{meta(when="13:30–13:45", who="Cả bàn", write="<code>TEAM.md</code>", out="Repo của bàn, <code>origin</code> và <code>upstream</code>, test đạt")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap">git clone https://github.com/&lt;trưởng-nhóm&gt;/K5-L3A-DAY10-XXX-PoCtoPilotGate1.git
cd K5-L3A-DAY10-XXX-PoCtoPilotGate1
git remote add upstream https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student.git
python3 -m unittest discover -s tests</pre>
    <section class="panel">
      <h3>Cần có</h3>
      <p>Python 3 và Git. Không cần cài gói. Không cần tài khoản hay API key.</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "<b>Chọn tài liệu chung từ Lab 9:</b> Chọn một eval card và một PRD v1.1. Cả bàn dùng hai tài liệu này.",
        "<b>Chia ba vai:</b> Ghi vai của mỗi người vào <code>TEAM.md</code>.",
        "<b>Trên Windows:</b> Nếu <code>python3</code> không chạy, dùng <code>python</code>.",
    )}
    {anti(
        "Một người làm hết, ba người ngồi xem.",
        "Bỏ bước gắn <code>upstream</code>.",
    )}
    {check("Có <code>Ran 13 tests</code> và <code>OK</code> không? <code>git remote -v</code> có <code>origin</code> và <code>upstream</code> không?")}
  </div>
</div>
""",
    """
<strong>Việc của coach trong CP1</strong>
<ul>
  <li>Bàn cần mạng ở bốn lúc: tạo và clone repo, push tiêu chí, kéo thẻ lúc 15:35, push bài nộp.</li>
  <li>Nhắc bàn kiểm wifi ngay bây giờ.</li>
  <li>Lab đã chạy thử trên Python 3.9.6 và 3.15.</li>
  <li>Nếu cài đặt lỗi, mở <code>docs/guide.md</code>, mục FAQ và mục Cài đặt.</li>
  <li>Bàn xong sớm: đọc tình huống LogiX-VN trong <code>problem-set.md</code> Phần A.</li>
  <li>Bàn xong sớm: mở <code>data/world.json</code>, đọc <code>staff</code>, <code>ops_limits</code>, <code>ops_facts</code>.</li>
</ul>
""",
    cp="1",
    minutes=15,
    label="CP1 · Cài đặt",
)

# 8 ── CP2 ───────────────────────────────────────────────────────────────
slide(
    "CP2: Viết tiêu chí, rồi ký",
    f"""
<h2 class="title">CP2: viết tiêu chí, ký trước lần chạy đầu tiên</h2>
{meta(when="13:45–14:35", who="Sản phẩm và kinh doanh viết chính", write="Phiếu A, <code>config/acceptance_criteria.json</code>", out="Tiêu chí đã ký và push")}
<div class="cp-layout">
  <div class="stack">
    <section class="panel">
      <h3>Câu 1.1–1.6 (13:45–14:30). Chưa chạy trợ lý.</h3>
      <p><b>Vì sao ký trước:</b> nếu bàn xem kết quả trước, bàn dễ đặt ngưỡng vừa khớp kết quả.</p>
      <p>Viết mục tiêu của hệ thống. Viết mục tiêu của chị Oanh (kế toán) và chị Hạnh (trưởng ca CSKH). Viết một chỉ số offline và một chỉ số production. Viết câu “Nếu … thì chúng tôi sẽ …”.</p>
    </section>
<pre class="code"><span class="c"># 14:30–14:35, ngay khi viết xong</span>
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json \\
        config/acceptance_criteria.lock
git commit -m 'Sign acceptance criteria'
git push -u origin main</pre>
  </div>
  <div class="stack">
    {coach(
        "<b>Điền đủ các trường:</b> Điền <code>team</code> (bằng tên repo) và <code>signed_by</code>. Điền 5 ngưỡng trong <code>required</code>, <code>nice_to_have</code>, nhóm <code>business_ops</code>, <code>stop_condition</code> và bốn dòng <code>decision_rule</code>.",
        "<b>Không chép ngưỡng của file mẫu:</b> File <code>acceptance_criteria.example.json</code> chỉ cho cách viết. Lấy con số từ <code>data/world.json</code>, mục <code>ops_facts</code>.",
        "<b>Chỉ số an toàn có thể là 0:</b> hoàn tiền sai, ghi lỗi sai cho hãng, lộ dữ liệu cá nhân.",
    )}
    {anti(
        "Chạy <code>eval</code> để “xem thử” trước khi ký.",
        "Ký xong mà không push ngay.",
    )}
    {check("Máy in <code>ĐÃ KÝ.</code> chưa? Commit ký có trên GitHub chưa? Phiếu A mục A5 có giờ ký và mã commit chưa?")}
  </div>
</div>
""",
    """
<strong>Vì sao bàn ký trước</strong>
<ul>
  <li>Bàn viết ngưỡng khi chưa ai biết trợ lý đạt hay không đạt.</li>
  <li>Lệnh <code>eval</code> và <code>grade</code> không chạy khi bàn chưa ký.</li>
  <li>Câu 1.6 có thêm hai câu giới hạn. Câu 1: một hành động trợ lý không được làm. Câu 2: ngưỡng chuyển ca cho người duyệt.</li>
  <li>Hai câu này không thêm trường JSON.</li>
  <li>Bàn soát bốn câu hỏi: có ích cho mọi bên không? Ai bị thiệt? Ngày 1 ra sao? Ngày 1.000 ra sao?</li>
  <li>Lỗi thường gặp: <code>Chưa ký được: thiếu team hoặc ngưỡng bắt buộc</code>. Nghĩa là <code>required</code> còn <code>null</code>.</li>
</ul>
""",
    cp="2",
    minutes=50,
    label="CP2 · Tiêu chí",
    done=1,
)

# 9 ── Three stages ──────────────────────────────────────────────────────
slide(
    "Ba mốc đo: base, prepared, after",
    """
<h2 class="title">Ba mốc đo trên cùng một bộ ticket</h2>
<div class="grid grid-3">
  <section class="panel"><h3>base</h3><p>Không có cổng của bàn. Trợ lý chạy như bản PoC.</p><p class="cp-ref">Đo ở CP3, câu 2.1</p></section>
  <section class="panel"><h3>prepared</h3><p>Chỉ có cổng vòng 1 đã chốt bằng lệnh 5. Bàn chưa biết sự cố.</p><p class="cp-ref">Đo ngay sau khi nhận thẻ, câu 3.0</p></section>
  <section class="panel"><h3>after</h3><p>Có cổng hiện tại, sau khi bàn sửa ở vòng 2.</p><p class="cp-ref">Đo sau khi sửa, câu 3.5</p></section>
</div>
<table class="data data--compact">
  <thead><tr><th>Report cho biết</th><th>Bàn dùng để</th></tr></thead>
  <tbody>
    <tr><td><code>pass_rate</code>, <code>pass_k</code> (đúng ở cả 5/5 seed)</td><td>So với ngưỡng đã ký</td></tr>
    <tr><td>Thời gian chờ duyệt, số ca bị ùn, chi phí mỗi ticket, ROI, tiền hoàn so với trần</td><td>Tìm dòng vượt trần</td></tr>
    <tr><td>Số đo theo kho và theo hãng</td><td>Quyết định có thu hẹp phạm vi không</td></tr>
  </tbody>
</table>
""",
    """
<strong>Giải thích ba mốc</strong>
<ul>
  <li>Bộ nền có 22 ticket. Mỗi ticket chạy với 5 seed.</li>
  <li><code>pass_k</code> là pass^k: ticket phải đúng ở cả 5 lần chạy. Chỉ số này chặt hơn <code>pass_rate</code>.</li>
  <li><code>pass_k</code> khác <code>pass@k</code>. <code>pass@k</code> chỉ cần đúng một lần.</li>
  <li>Khi demo, bàn chiếu ba cột này. Bàn nói cổng vòng 1 chặn được gì, và phần nào phải sửa sau.</li>
  <li>Dòng cuối report có hai giá trị: “được phép cân nhắc Tiếp tục” hoặc “không đủ căn cứ”.</li>
  <li>Kết quả tự kiểm tra (<code>FAIL</code>, <code>PARTIAL</code>, <code>PASS-VISIBLE</code>) chỉ cho biết bàn sửa được bao nhiêu. Kết quả này không bắt bàn chọn Tiếp tục.</li>
</ul>
""",
    done=2,
)

# 10 ── CP3 ──────────────────────────────────────────────────────────────
slide(
    "CP3: Đo, tìm rủi ro, viết cổng vòng 1",
    f"""
<h2 class="title">CP3: đo base, tìm rủi ro, viết cổng vòng 1</h2>
{meta(when="14:35–15:25", who="Ba vai làm song song", write="Phiếu B, mục B0–B8", out="Mã lần chạy base, 2–3 cổng, cổng trong config, v1")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap"><span class="c"># 2A · 14:35–14:55. Chưa sửa code. Chưa sửa config.</span>
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/&lt;mã&gt;/report.json
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
<span class="c"># 2B · 14:55–15:15. Viết cổng.</span>
python3 -m lab10.eval --suite base --stage after --note "cổng v1"</pre>
    <section class="panel">
      <h3>Ở 2A, mỗi vai làm một việc</h3>
      <p>Kỹ sư cổng: câu 2.1–2.2. Kinh doanh: bản đồ dữ liệu, một ví dụ drift (2.3). Vận hành: HAZOP và checklist 9 nhóm việc (2.4). Cả bàn: pre-mortem (2.5).</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "<b>Mỗi cổng có một lý do:</b> Mỗi cổng trong <code>pre_guard</code> hoặc <code>write_gate</code> phải ứng với một lý do pre-mortem hoặc một dòng HAZOP.",
        "<b>Một số cổng không cần code:</b> Ghi vào <code>config/operating_gates.json</code>: trần tiền hoàn mỗi ngày, ngân sách mỗi ticket, phạm vi pilot, người trực, thời gian chờ tối đa.",
        "<b>Viết một test hành vi:</b> Viết 2 ticket mới. Chạy bằng <code>--adhoc</code>. Giữ 2 ticket này cho phần demo (câu 2.8).",
    )}
    {anti(
        "Sửa cổng tới khi cả 22 ticket đạt. Đây là rò rỉ dữ liệu.",
        "Cổng làm sai một ticket đang đúng.",
    )}
    {check("Bàn đã xếp loại lỗi cho <code>T-002@55</code> chưa? Pre-mortem có đủ bốn lăng kính chưa? Test công khai còn đạt không?")}
  </div>
</div>
""",
    """
<strong>Việc của coach trong CP3</strong>
<ul>
  <li>HAZOP cần ít nhất 3 dòng. Thêm ít nhất 2 dòng ngoài kỹ thuật.</li>
  <li>Checklist 9 nhóm việc: mỗi dòng có một người phụ trách có tên.</li>
  <li>Câu 2.1 hỏi thêm: cổng tự chặn bản phát hành, hay người duyệt chặn? Bàn ghi lý do của hai phía, rồi chọn một.</li>
  <li>Câu 2.7: bàn ghi 2 bước để không rò rỉ dữ liệu. Gắn với bộ nền, thẻ sự cố và test ẩn.</li>
  <li>Câu 2.10: runbook phần 1–3 phải dùng đúng con số trong config.</li>
  <li>Runbook ghi thời hạn dừng: từ tín hiệu đỏ tới lúc dừng xong là bao nhiêu phút, và ai bấm dừng.</li>
  <li>Runbook có mục Giờ cao điểm: ai trực, mấy người, khi nào gọi thêm người, khi nào thu hẹp hay tắt.</li>
  <li>Ví dụ viết cổng: <code>docs/guide.md</code>, Phụ lục C. Hàm tra cứu: <code>lab10/helpers.py</code>.</li>
</ul>
""",
    cp="3",
    minutes=50,
    label="CP3 · Rủi ro và cổng",
    done=2,
)

# 11 ── Lock round 1 ─────────────────────────────────────────────────────
slide(
    "Chốt vòng 1 và quyết định v1",
    """
<h2 class="title">15:15–15:25: chốt cổng vòng 1, viết quyết định v1</h2>
<ol class="loop loop--three">
  <li><b>Chốt cổng</b><span>Chạy <code>python3 -m lab10.checkpoint</code>. Lệnh lưu một bản của <code>guards.py</code> và <code>operating_gates.json</code>.</span></li>
  <li><b>Đo prepared</b><span>Chạy <code>eval --suite base --stage prepared</code>. Chạy <code>gate --run …</code>.</span></li>
  <li><b>Viết v1 và push</b><span>Phiếu B mục B8: quyết định, ba dòng số đo có mã lần chạy, dòng <code>decision_rule</code>.</span></li>
</ol>
<div class="grid grid-2">
  <section class="panel"><h3>Ba câu hỏi trước khi quyết định</h3><p>Rủi ro còn lại có chấp nhận được không? Cần thêm cổng nào, mất bao lâu? Phần nào không nên làm tiếp?</p></section>
  <section class="anti"><h3>{ICONS_ANTI}Sau mốc này</h3><ul><li>Không sửa v1.</li><li>Không sửa hai file bản chốt vòng 1.</li></ul></section>
</div>
<p class="note"><b>Vì sao chốt:</b> ở vòng 2, lab so bản chốt với bản sửa. Nếu bàn sửa được bản chốt, phép so này không còn ý nghĩa.</p>
""",
    """
<strong>Chuyển sang vòng 2</strong>
<ul>
  <li>Lúc 15:05, báo lớp còn 10 phút để chốt.</li>
  <li>Bàn không chốt sẽ không có mốc prepared. Cuối buổi, lệnh 7 sẽ báo thiếu.</li>
  <li>Bàn đã ký tiêu chí lúc 14:30–14:35. Bàn không ký lại.</li>
  <li>Nhắc bàn commit và push trước giờ nghỉ.</li>
</ul>
""",
    done=3,
)

# 12 ── Incident drop ────────────────────────────────────────────────────
slide(
    "Phát thẻ sự cố",
    """
<h2 class="title">15:35: phát thẻ sự cố S1–S8</h2>
<pre class="code code--wrap">git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main
python3 -m lab10.grade --incident Sx   <span class="c"># chạy trước khi sửa</span></pre>
<div class="grid grid-2">
  <section class="panel">
    <h3>Mỗi cặp bàn bốc một số</h3>
    <p>Hai bàn trong cặp làm cùng một thẻ. Mở <code>incidents/Sx/card.md</code>. Ghi số thẻ vào dòng <code>Thẻ đã bốc:</code> ở đầu Phiếu C.</p>
  </section>
  <section class="panel">
    <h3>Tám thẻ, tám tác hại</h3>
    <p>Năm thẻ có nguyên nhân chính ở kỹ thuật. Ba thẻ có nguyên nhân chính ở kinh doanh hoặc con người.</p>
  </section>
</div>
<p class="note"><b>Vì sao đo trước khi sửa:</b> lần đo này là mốc prepared. Nếu bàn sửa trước, bàn mất mốc này và không biết cổng vòng 1 đỡ được bao nhiêu.</p>
<p class="note">Coach đọc: “Sáng nay bàn nhận tin nhắn này. Tiêu chí đã ký không đổi. Sau 60 phút, bàn cho tôi biết: quyết định Gate 1 còn đúng không?”</p>
""",
    """
<strong>Các bước phát thẻ</strong>
<ul>
  <li>Đẩy thẻ lên repo mẫu. Sau đó báo lớp: “Đã phát thẻ”.</li>
  <li>Bàn kéo trước giờ sẽ thấy <code>Already up to date</code>. Bàn chờ, rồi kéo lại.</li>
  <li>Lỗi <code>'upstream' does not appear to be a git repository</code>: làm lại bước 2a.</li>
  <li>Lỗi <code>Please tell me who you are</code>: làm bước 2b.</li>
  <li>Xung đột khi kéo: chạy <code>git merge --abort</code>, rồi chạy lại đủ lệnh.</li>
  <li>Kéo đúng thì report có <code>1 integrity | ✅</code>.</li>
  <li>Lab Coach ghi số thẻ của từng cặp vào sổ.</li>
  <li>Ba thẻ kinh doanh hoặc con người: hàng chờ quá dài, chi phí cao hơn làm tay, nhân viên không tin trợ lý.</li>
  <li>Với ba thẻ đó, bàn sửa chủ yếu ở phạm vi, nhân sự, cách giải thích và quy trình. Code là phần nhỏ.</li>
</ul>
""",
    done=3,
)

# 12b ── Read the report ─────────────────────────────────────────────────
slide(
    "Đọc report của lệnh 6",
    """
<h2 class="title">Đọc report của lệnh 6: sáu dòng</h2>
<table class="data data--compact">
  <thead><tr><th>Dòng</th><th>Câu hỏi</th><th>✅ khi</th></tr></thead>
  <tbody>
    <tr><td class="num">1 integrity</td><td>Bàn có sửa file khóa hoặc bản chốt vòng 1 không?</td><td>Không sửa. Nếu ❌, bài bị 0 điểm.</td></tr>
    <tr><td class="num">2 criteria</td><td>Tiêu chí còn giống lúc ký không?</td><td>Còn nguyên.</td></tr>
    <tr><td class="num">3 visible</td><td>Thẻ sự cố đã sạch chưa?</td><td>Base có lỗi. After không còn lỗi. Độ phủ pilot lớn hơn 0.</td></tr>
    <tr><td class="num">4 hidden</td><td>Phần sửa có qua test ẩn không?</td><td>Trên máy bàn hiện “—”. Team chấm chạy sau buổi.</td></tr>
    <tr><td class="num">5 regression</td><td>Có ca nào trước đúng, giờ sai không?</td><td>Không có ca mới hỏng. Độ phủ pilot lớn hơn 0.</td></tr>
    <tr><td class="num">6 monitor</td><td>Bàn có chỉ số theo dõi mới không?</td><td>Có ít nhất một chỉ số trong <code>lab10/monitors.py</code>.</td></tr>
  </tbody>
</table>
<section class="panel panel--warn">
  <h3>Ba cách không được tính là sửa</h3>
  <p>Chặn hết. Thu hẹp phạm vi về 0. Xếp thật nhiều người trực. Report đo cả độ phủ, chi phí và ROI, nên bàn không qua được bằng ba cách này.</p>
</section>
""",
    """
<strong>Cách đọc report</strong>
<ul>
  <li>Report có ba cột: <code>base · prepared · after</code>. Đọc từ trái sang phải.</li>
  <li>Cột prepared cho biết cổng vòng 1 đỡ được bao nhiêu. Cột after cho biết phần sửa có tác dụng không.</li>
  <li>Vì sao cần độ phủ lớn hơn 0: nếu trợ lý không xử lý ticket nào, không ticket nào sai. Nhưng khi đó trợ lý không có ích.</li>
  <li>Phần cuối report ghi các dòng còn vượt trần. Bàn đọc phần này trước khi viết v2.</li>
  <li>Bảng theo kho có cột chi phí mỗi ticket. Bàn dùng cột này cho dòng kho xấu nhất ở B8 và C12.</li>
</ul>
""",
    done=3,
)

# 13 ── CP4 ──────────────────────────────────────────────────────────────
slide(
    "CP4: Thẻ sự cố: tìm nguyên nhân và sửa",
    f"""
<h2 class="title">CP4: một tác hại, nhiều nguyên nhân</h2>
{meta(when="15:35–16:35", who="Cả bàn", write="Phiếu C, mục C0–C11", out="Report ba mốc, một chỉ số theo dõi mới")}
<div class="cp-layout">
  <div class="stack">
<table class="data data--compact">
  <thead><tr><th>Giờ</th><th>Việc</th></tr></thead>
  <tbody>
    <tr><td class="num">15:35</td><td>3.0 Đo prepared. Ghi cổng vòng 1 chặn được gì.</td></tr>
    <tr><td class="num">15:45</td><td>3.1–3.4 Trace ít nhất 2 ticket. Viết HAZOP của thẻ, spec, giả định môi trường, cây lỗi.</td></tr>
    <tr><td class="num">16:05</td><td>3.5–3.6 Sửa đúng chỗ. Thêm một hàm vào <code>MONITORS</code>.</td></tr>
    <tr><td class="num">16:30</td><td>3.7 Vẽ lại cây lỗi. Viết risk register, runbook 4–5.</td></tr>
  </tbody>
</table>
<pre class="code code--wrap">python3 -m lab10.trace --suite Sx --ticket &lt;ID&gt; --seed 11
python3 -m lab10.eval --suite Sx --stage after --note "…"
python3 -m lab10.grade --incident Sx</pre>
  </div>
  <div class="stack">
    {coach(
        "<b>Ghi ai bị hại và đo bằng gì:</b> Trước khi sửa, ghi bên bị hại và con số ở mốc base.",
        "<b>Cây lỗi có hai tầng:</b> Vẽ ít nhất hai nhánh ở hai tầng khác nhau: kỹ thuật, kinh doanh, con người. Mỗi lá có bằng chứng: <code>ticket@seed</code> hoặc một dòng report.",
        "<b>Ghi giảm hay ngăn:</b> Với mỗi cách sửa, ghi rõ: cách này giảm khả năng, hay ngăn hẳn tác hại.",
    )}
    {anti(
        "Sửa trước khi đo prepared.",
        "Thẻ về con người mà chỉ sửa code.",
        "Ghi đè HAZOP vòng 1.",
        "Thu hẹp phạm vi về 0 để report hết đỏ.",
    )}
    {check("Report có <code>visible ✅</code>, <code>regression ✅</code>, <code>monitor ✅</code> không? Độ phủ pilot lớn hơn 0 không? Còn dòng nào vượt trần không?")}
  </div>
</div>
""",
    """
<strong>Việc của coach trong CP4</strong>
<ul>
  <li>Bảng soát lỗi cần ít nhất 2 lỗi từ 2 nguồn khác nhau. Cần ít nhất 1 lỗi ẩn.</li>
  <li>Vai Vận hành và pháp lý viết phần riêng của thẻ (mục C3). Thẻ S4 không dùng C3: phần riêng nằm ở C1 và Phiếu B mục B7.6.</li>
  <li>Bàn sửa ở ba chỗ. Chỗ 1: code trong <code>lab10/guards.py</code>.</li>
  <li>Chỗ 2: con số và quy trình trong <code>config/operating_gates.json</code>. Ví dụ: phạm vi, người trực, trần, ngân sách, kiểm mẫu, cổng pháp lý.</li>
  <li>Chỗ 3: người.</li>
  <li>Chỉ số theo dõi mới có thể là kỹ thuật, vận hành hoặc kinh doanh.</li>
  <li>Bàn viết đủ ba ô: thước đo, dữ liệu, cách tính (mục C8).</li>
  <li>Report tự kiểm tra có sáu mục: file khóa, tiêu chí, thẻ sự cố, test ẩn, bộ nền, chỉ số theo dõi.</li>
  <li>Trên máy của bàn, mục test ẩn hiện “—”. Team chấm chạy mục này sau buổi.</li>
  <li>Nếu độ phủ pilot bằng 0, hai mục <code>visible</code> và <code>regression</code> báo ❌. Thu hẹp về 0 không phải cách sửa.</li>
  <li>Bảng theo kho có thêm cột chi phí mỗi ticket. Bàn dùng cột này cho dòng kho xấu nhất ở B8 và C12.</li>
</ul>
""",
    cp="4",
    minutes=60,
    label="CP4 · Sự cố",
    done=3,
)

# 14 ── Decisions ────────────────────────────────────────────────────────
slide(
    "Bốn quyết định Gate 1",
    """
<h2 class="title">Quyết định v2: đạt khi khớp số đo</h2>
<table class="data">
  <thead><tr><th>Quyết định</th><th>Đạt khi</th><th>Không đạt khi</th></tr></thead>
  <tbody>
    <tr><td class="num">Tiếp tục</td><td>Mọi ngưỡng đã ký đều đạt. Không dòng nào vượt trần.</td><td>Report còn vượt trần. Hoặc còn ngưỡng chưa đạt.</td></tr>
    <tr><td class="num">Thu hẹp</td><td>Ghi rõ: bỏ kho nào, còn bao nhiêu phần trăm, mấy người trực, ticket bị bỏ đi đâu.</td><td>Thu hẹp về 0.</td></tr>
    <tr><td class="num">Cải tiến thêm</td><td>Có giả thuyết cụ thể. Có hạn chót.</td><td>Chỉ ghi “cần thêm thời gian”.</td></tr>
    <tr><td class="num">Dừng</td><td>Có lý do. Có con số. Có bài học.</td><td>Không chỉ ra con số nào.</td></tr>
  </tbody>
</table>
<h3 class="sub">Ba dòng bắt buộc (Phiếu C mục C12, chép vào <code>submission.json</code>)</h3>
<ol class="loop loop--three">
  <li><b>Giả định môi trường</b><span>Một điều thiết kế đang tin, có thể sai ngoài thực tế.</span></li>
  <li><b>Giảm hay ngăn</b><span>Cổng chỉ giảm khả năng, hay ngăn hẳn tác hại. Vì sao.</span></li>
  <li><b>Đo lại khi chạy thử</b><span>Dữ liệu là giả. Ghi chỉ số cần đo lại trước Gate 2.</span></li>
</ol>
""",
    """
<strong>Điều kiện qua</strong>
<ul>
  <li>Quyết định phải khớp số đo và khớp tiêu chí đã ký.</li>
  <li>Đây là điều kiện để bài được tính. Đây không phải điểm cộng.</li>
  <li>Cột v2 ghi thêm: đổi hay giữ so với v1, vì con số nào, mã lần chạy của ba mốc.</li>
  <li>Khi đi qua từng bàn, hỏi: “Con số nào trong report cho quyết định này?”</li>
</ul>
""",
    done=4,
)

# 15 ── CP5 ──────────────────────────────────────────────────────────────
slide(
    "CP5: Quyết định v2, demo, nộp",
    f"""
<h2 class="title">CP5: quyết định v2, demo ba mốc, nộp bài</h2>
{meta(when="16:35–17:30", who="Cả bàn", write="Phiếu C mục C12, <code>submission/submission.json</code>", out="Lệnh 7 in <code>ĐỦ THÀNH PHẦN</code>")}
<div class="cp-layout">
  <div class="stack">
<table class="data data--compact">
  <thead><tr><th>Giờ</th><th>Việc</th></tr></thead>
  <tbody>
    <tr><td class="num">16:35</td><td>Viết v2. Điền <code>submission.json</code>. Chạy lệnh 7 tới khi đủ.</td></tr>
    <tr class="row-key"><td class="num">16:50</td><td>Demo: hai bàn cùng thẻ ngồi cặp. Mỗi bàn 5 phút. 2–3 bàn trình bày trước lớp.</td></tr>
    <tr><td class="num">17:20</td><td>Trả con số về bản v2. Chạy lại lệnh 6 và 7. Push.</td></tr>
  </tbody>
</table>
<pre class="code">python3 -m lab10.check_submission --collect
git add -u
git add submission templates TEAM.md
git commit -m "LAB 10: bài nộp"
git push -u origin main</pre>
  </div>
  <div class="stack">
    {coach(
        "<b>Chiếu ba cột khi demo:</b> Chiếu base · prepared · after. Nói cổng vòng 1 chặn được gì. Nói phần sửa là code, con số hay người.",
        "<b>Bàn kia hỏi lại:</b> Bàn kia chạy một ticket khó (câu 2.8) bằng <code>--adhoc</code>. Hoặc bàn kia đổi một con số trong <code>operating_gates.json</code>, rồi chạy lại.",
        "<b>Ghi MSSV trong members:</b> Ghi dạng <code>&quot;HoVaTen-MSSV&quot;</code>. Tên phải khớp <code>TEAM.md</code>.",
    )}
    {anti(
        "Không trả con số demo về bản v2 trước khi gom bài.",
        "Chỉ trưởng nhóm nộp link LMS.",
    )}
    {check("Lệnh 7 có báo mục phiếu nào còn nguyên mẫu không? Lệnh 7 in <code>ĐỦ THÀNH PHẦN</code> trên code và config cuối cùng không?")}
  </div>
</div>
""",
    """
<strong>Việc của coach trong CP5</strong>
<ul>
  <li>Sau demo, nếu bàn không chạy lại lệnh 6, lệnh 7 báo: “báo cáo không chạy trên đúng code và config hiện tại”.</li>
  <li>Lệnh 7 báo tên từng mục phiếu còn nguyên mẫu (A1–A5, B0–B8, C0–C12). Bàn điền mục đó, rồi chạy lại lệnh 7.</li>
  <li>Sau khi push, kiểm trên GitHub: <code>submission/runs/</code> có <code>journal.jsonl</code> và report ba mốc.</li>
  <li>Lab Coach hỏi theo phiếu thẻ. Lab Coach không cho điểm.</li>
  <li>Ghi lại câu trả lời demo cho team chấm.</li>
  <li>Cuối buổi, mỗi người viết exit ticket trong mục cá nhân của <code>TEAM.md</code>.</li>
  <li>Mỗi người tự nộp link repo trên LMS.</li>
  <li>Không push vào repo mẫu (<code>upstream</code>).</li>
</ul>
""",
    cp="5",
    minutes=55,
    label="CP5 · v2 và nộp",
    done=4,
)

# 16 ── Seven commands ───────────────────────────────────────────────────
slide(
    "Bảy lệnh của lab",
    """
<h2 class="title">Bảy lệnh và lúc dùng</h2>
<table class="data data--compact">
  <thead><tr><th>#</th><th>Lệnh</th><th>Dùng khi</th></tr></thead>
  <tbody>
    <tr><td class="num">1</td><td><code>python3 -m lab10.criteria sign</code></td><td>Ký tiêu chí. Một lần, lúc 14:30–14:35.</td></tr>
    <tr><td class="num">2</td><td><code>python3 -m lab10.eval --suite … --stage … --note "…"</code></td><td>Chạy trợ lý trên một bộ ticket. Lệnh in mã lần chạy.</td></tr>
    <tr><td class="num">3</td><td><code>python3 -m lab10.trace --suite … --ticket … --seed …</code></td><td>Xem từng bước của một ticket. Hoặc dùng <code>--adhoc</code>.</td></tr>
    <tr><td class="num">4</td><td><code>python3 -m lab10.gate --run runs/&lt;mã&gt;/report.json</code></td><td>So một lần chạy với tiêu chí đã ký.</td></tr>
    <tr><td class="num">5</td><td><code>python3 -m lab10.checkpoint</code></td><td>Chốt cổng vòng 1. Một lần, lúc 15:15–15:25.</td></tr>
    <tr><td class="num">6</td><td><code>python3 -m lab10.grade --incident Sx</code></td><td>Tự kiểm tra trên thẻ ở ba mốc. Từ 15:35.</td></tr>
    <tr><td class="num">7</td><td><code>python3 -m lab10.check_submission --collect</code></td><td>Gom bài nộp. Kiểm đủ thành phần.</td></tr>
  </tbody>
</table>
""",
    """
<strong>Tra cứu</strong>
<ul>
  <li>Kết quả mẫu và cách đọc: <code>docs/guide.md</code>, Phụ lục A–B và mục “Các mẫu kết quả đầy đủ”.</li>
  <li>Seed dùng được cho trace: 11, 22, 33, 44, 55.</li>
  <li>Khi lệnh có <code>&lt;mã lần chạy&gt;</code>, thay cả dấu ngoặc nhọn bằng mã máy vừa in.</li>
</ul>
""",
    done=4,
)

# 17 ── Rubric ───────────────────────────────────────────────────────────
RUBRIC_ROWS = [
    ("C1", "Tiêu chí và cách đo (Phiếu A)", "CP2", 15),
    ("C2", "Rủi ro trước sự cố", "CP3", 15),
    ("C3", "Cổng vòng 1 và quyết định v1", "CP3", 15),
    ("C4", "Số đo trên thẻ và test ẩn", "CP4", 25),
    ("C5", "Tìm nguyên nhân và sửa", "CP4", 20),
    ("C6", "Quyết định v2 và ba dòng", "CP5", 10),
]
_rubric = "\n".join(
    f'      <tr><td><b>{c}</b> {name}</td><td>{cp}</td><td class="bar-cell" title="{pts} điểm"><span class="bar" style="--v: {pts / 25:.3f}"></span><span class="bar-val">{pts}</span></td></tr>'
    for c, name, cp, pts in RUBRIC_ROWS
)
slide(
    "Rubric: 100 điểm, C1 đến C6",
    f"""
<h2 class="title">Rubric: 100 điểm, C1 đến C6</h2>
<div class="grid grid-rubric">
  <table class="data data--compact">
    <thead><tr><th>Tiêu chí chấm</th><th>Checkpoint</th><th>Điểm</th></tr></thead>
    <tbody>
{_rubric}
    </tbody>
  </table>
  <div class="stack">
    <section class="anti">
      <h3>{{ICONS_ANTI}}Bài không qua khi</h3>
      <ul>
        <li>Bàn ký sau khi đo, hoặc sửa sau khi ký.</li>
        <li>Bàn sửa file khóa hoặc bản chốt.</li>
        <li>Quyết định không khớp số đo.</li>
        <li>Lệnh 7 chưa in <code>ĐỦ THÀNH PHẦN</code>.</li>
      </ul>
    </section>
    <p class="note">Điểm thưởng: tối đa +10, ghi riêng.</p>
  </div>
</div>
""",
    """
<strong>Cách chấm (RUBRIC.md, bản đề xuất trong PR #1, chưa duyệt)</strong>
<ul>
  <li>Team chấm chấm ba phần (<code>problem-set.md</code> phần D).</li>
  <li>Phần 1, máy đo: test ẩn, chỉ số kinh doanh và vận hành, mốc prepared, hash, các ca đang đúng.</li>
  <li>Phần 2, người đọc: pre-mortem, HAZOP, checklist có người phụ trách, runbook, Phiếu C, ba dòng, câu trả lời demo.</li>
  <li>Phần 3: điều kiện qua.</li>
  <li>Điểm thưởng: cổng vòng 1 chặn được phần lớn sự cố (+5). Chỉ số hoặc cổng tìm ra lỗi ẩn ngoài thẻ, có trace (+5).</li>
  <li>Trừ điểm: thiếu mục cá nhân trong <code>TEAM.md</code>. <code>members</code> thiếu MSSV (−5). Sai tên repo, hoặc <code>team</code> không khớp (−5).</li>
  <li>Nếu điểm chính thức khác, sửa <code>RUBRIC_ROWS</code> trong <code>content/build_content.py</code>, rồi build lại.</li>
</ul>
""",
    done=5,
)

# 18 ── Submit checklist ─────────────────────────────────────────────────
slide(
    "Checklist nộp bài",
    """
<h2 class="title">Checklist nộp bài</h2>
<div class="grid grid-2">
  <div>
    <h3 class="sub">Trước khi nộp, kiểm:</h3>
    <ul class="checklist">
      <li>Tên repo là <code>K5-L3A-DAY10-…-PoCtoPilotGate1</code> hoặc <code>K5-L3B-DAY10-…-PoCtoPilotGate1</code>. Đã mời team chấm.</li>
      <li><code>TEAM.md</code> có họ tên, MSSV, vai và mục cá nhân của mỗi người.</li>
      <li>Bàn đã ký và push tiêu chí trước lần chạy đầu tiên.</li>
      <li>Bàn đã chốt vòng 1. Ba phiếu A, B, C đã điền mọi mục.</li>
      <li><code>submission.json</code> đủ trường. <code>members</code> có MSSV.</li>
      <li>Lệnh 7 in <code>ĐỦ THÀNH PHẦN</code>. Trên GitHub có <code>submission/runs/</code>.</li>
      <li>Repo không có <code>.env</code> hay key.</li>
      <li>Mỗi người đã nộp link trên LMS.</li>
    </ul>
  </div>
  <div class="stack">
    <section class="panel">
      <h3>Hạn nộp (GMT+7)</h3>
      <p class="deadline">{{DEADLINE}}</p>
      <p>Push bài trong buổi trước 17:30. Coach có thể gia hạn tối đa 48 giờ.</p>
    </section>
    <div class="cta-row">
      <button class="btn-primary" type="button" onclick="window.kickoffLab && window.kickoffLab()">Bắt đầu CP1: Cài đặt</button>
    </div>
  </div>
</div>
""",
    """
<strong>Lời dặn cuối</strong>
<ul>
  <li>Bấm nút để về CP1 và bắt đầu.</li>
  <li>Hạn nộp (GMT+7): lớp sáng 23h59 ngày lab. Lớp chiều 11h59 sáng hôm sau.</li>
  <li>Slide tự hiện hạn nộp của ca đang mở.</li>
  <li>Team chấm lấy commit cuối cùng trước hạn. Commit sau hạn không được tính.</li>
  <li>Lỗi kỹ thuật sau buổi: gửi mô tả lỗi, ảnh lệnh và kết quả, trước hạn nộp.</li>
</ul>
""",
    done=5,
)

out = pathlib.Path(__file__).resolve().parent.parent / "app/src/slides/content.json"
out.write_text(json.dumps(S, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {len(S)} slides -> {out}")
