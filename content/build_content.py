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
        notes = notes.strip() + f"\n<strong>Coach nói gì (chi tiết)</strong>\n<ul>{extra}</ul>"
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
        "time": "Timebox",
        "when": "Khung giờ",
        "who": "Ai làm",
        "write": "Ghi vào",
        "out": "Sản phẩm",
        "bonus": "Bonus",
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
    return f'<section class="coach"><h3>{ICONS["coach"]}Coach nói gì</h3><ul>{li}</ul></section>'


def anti(*items):
    li = "".join(f"<li>{x}</li>" for x in items)
    return f'<section class="anti"><h3>{ICONS["anti"]}Anti-pattern thường gặp</h3><ul>{li}</ul></section>'


def check(text):
    return f'<section class="selfcheck"><h3>{ICONS["check"]}Tự kiểm tra</h3><p>{text}</p></section>'


# 0 ── Title ─────────────────────────────────────────────────────────────
slide(
    "Day 10: From PoC to Pilot (Gate 1)",
    """
<div class="title-slide">
  <div class="title-copy">
    <p class="course">VinUni AI20k, K5 Level 3 (3A và 3B), {{SESSION}}, {{SESSION_RANGE}}</p>
    <h1 class="hero">Ký tiêu chí trước, xem số sau, quyết định khớp bằng chứng</h1>
    <p class="lede">Bàn làm hồ sơ Gate 1 cho trợ lý hoàn tiền giao trễ của LogiX-VN: có đủ tin cậy để chạy thử với khách thật ở 2 depot không?</p>
  </div>
  <figure class="title-proof">
    <figcaption>Ba mốc đo, chiếu khi demo cuối buổi:</figcaption>
<pre class="code code--big"><span class="c"># python3 -m lab10.grade --incident Sx</span>
            base   prepared   after
cổng của bàn  —     vòng 1    vòng 2
quyết định    —       v1        v2
<span class="c"># Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng</span></pre>
  </figure>
</div>
<div class="facts">
  <section><h2>Hình thức</h2><p>Bài nhóm, bàn 4–5 người, 240 phút.</p></section>
  <section><h2>Chấm điểm</h2><p>Không chấm tại lớp. Team chấm sau buổi, 100 điểm C1–C6, bonus tối đa 10.</p></section>
  <section><h2>Deadline</h2><p>{{DEADLINE}} (GMT+7).</p></section>
  <section><h2>Điều khiển</h2><p><kbd>←</kbd> <kbd>→</kbd> chuyển slide, <kbd>N</kbd> ghi chú.</p></section>
</div>
""",
    """
<strong>Chào lớp và neo tư duy</strong>
<ul>
  <li>Hôm nay không hỏi “model trả lời có hay không”. Câu hỏi là: <b>có đủ căn cứ để cho trợ lý chạy thử với khách thật không</b>, ai chịu trách nhiệm, tốn bao nhiêu tiền, cần mấy người trực.</li>
  <li>Bốn quyết định Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng đều có thể đạt, miễn là <b>khớp bằng chứng và khớp tiêu chí đã ký</b>.</li>
  <li>Không ai chấm điểm tại lớp. Các lệnh chỉ để bàn tự kiểm tra; team chấm đọc repo của bàn sau buổi học, kể cả bộ test ẩn.</li>
  <li>MockLLM tất định: mọi lần chạy tái lập được, không cần API key, không cần cài gói.</li>
</ul>
""",
)

# 1 ── Format ────────────────────────────────────────────────────────────
slide(
    "Hình thức: bàn ba vai, hai vòng",
    """
<h2 class="title">Một bàn, ba vai, hai vòng</h2>
<p class="lede">Vòng 1 bàn chưa biết sự cố. Vòng 2 bàn bốc thẻ và xem cổng đã chuẩn bị đỡ được bao nhiêu.</p>
<div class="grid grid-3 roles">
  <section class="panel"><h3>Kỹ sư cổng (1–2)</h3><p>Lệnh, trace, code cổng trong <code>lab10/guards.py</code>, chỉ số theo dõi trong <code>lab10/monitors.py</code>.</p></section>
  <section class="panel"><h3>Sản phẩm và kinh doanh (1–2)</h3><p>Tiêu chí để ký, cổng <code>business</code>, chi phí, ROI, quyết định v1 và v2.</p></section>
  <section class="panel"><h3>Vận hành và pháp lý (1)</h3><p>HAZOP, checklist 9 nhóm việc có PIC, cổng <code>operations</code> và <code>legal</code>, runbook, gom bài.</p></section>
</div>
<ol class="loop loop--three">
  <li><b>Vòng 1 · 13:45–15:25</b><span>Ký tiêu chí, đo base, tìm rủi ro, dựng cổng, chốt v1.</span></li>
  <li><b>Phát thẻ · 15:35</b><span>Mỗi cặp bàn bốc một thẻ S1–S8.</span></li>
  <li><b>Vòng 2 · 15:35–16:50</b><span>Đo prepared, phân tích, sửa, quyết định v2.</span></li>
</ol>
""",
    """
<strong>Cơ chế bàn</strong>
<ul>
  <li>Người không viết code vẫn có việc thật: tiêu chí, chi phí, số người trực, runbook, quyết định. Lab hỏi cả code đúng chưa, tốn bao nhiêu tiền, cần mấy người trực và ai chịu trách nhiệm.</li>
  <li>Bàn chỉ làm việc ở đúng các chỗ được liệt kê trong README mục 1; các file khác bị khoá bằng hash, sửa là lệnh tự kiểm tra phát hiện.</li>
  <li>Bảng thành viên giờ nằm trong <code>TEAM.md</code> (không còn ở README). Mỗi người viết mục <code>## HoVaTen-MSSV</code> của mình, gồm cả exit ticket.</li>
</ul>
""",
)

# 2 ── Goals ─────────────────────────────────────────────────────────────
slide(
    "Bốn mục tiêu học tập của Lab Day 10",
    """
<h2 class="title">Bốn mục tiêu học tập của Lab Day 10</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>Viết tiêu chí trước khi xem bằng chứng</h3>
    <p>Ngưỡng “Nếu … thì chúng tôi sẽ …”, ký và push trước lần đánh giá đầu tiên.</p>
    <p class="cp-ref">CP2, tiêu chí C1</p>
  </section>
  <section class="panel">
    <h3>Tìm rủi ro trước khi nó xảy ra</h3>
    <p>Pre-mortem bốn lăng kính, HAZOP có dòng ngoài kỹ thuật, checklist 9 nhóm việc có PIC.</p>
    <p class="cp-ref">CP3, tiêu chí C2</p>
  </section>
  <section class="panel">
    <h3>Dựng cổng ngoài model</h3>
    <p>Cổng bằng code, bằng con số trong config, và bằng người; không làm hỏng ca đang đúng.</p>
    <p class="cp-ref">CP3, CP4, tiêu chí C3, C4, C5</p>
  </section>
  <section class="panel">
    <h3>Quyết định Gate 1 khớp bằng chứng</h3>
    <p>v1 và v2 dựa trên report ba mốc và tiêu chí đã ký, kèm ba dòng bắt buộc.</p>
    <p class="cp-ref">CP5, tiêu chí C6</p>
  </section>
</div>
""",
    """
<strong>Bốn mục tiêu, gắn với RUBRIC.md (bản đề xuất trong PR #1)</strong>
<ul>
  <li>Mục tiêu 1 là điều kiện qua: tiêu chí ký sau khi đã chạy đánh giá, hoặc sửa sau khi ký, thì bài không được tính. Team chấm đối chiếu lịch sử git với <code>runs/journal.jsonl</code>.</li>
  <li>Mục tiêu 3: “chặn hết”, thu hẹp phạm vi về 0 hay xếp thật nhiều người trực không phải cách sửa; report đo cả độ phủ, chi phí và ROI.</li>
  <li>Mục tiêu 4: chọn Tiếp tục khi report còn vượt trần hoặc còn ngưỡng đã ký chưa đạt là quyết định không đạt.</li>
</ul>
""",
)

# 3 ── Schedule ──────────────────────────────────────────────────────────
slide(
    "Năm checkpoint và mốc giờ",
    """
<h2 class="title">Năm checkpoint và mốc giờ trong buổi</h2>
<table class="data">
  <thead><tr><th>Giờ</th><th>Checkpoint</th><th>Phải có trong repo</th><th>Phiếu</th></tr></thead>
  <tbody>
    <tr><td class="num">13:30</td><td><b>CP1</b> Cài đặt, chia vai</td><td><code>Ran 13 tests … OK</code>, <code>origin</code> và <code>upstream</code>, <code>TEAM.md</code></td><td>TEAM</td></tr>
    <tr class="row-key"><td class="num">13:45</td><td><b>CP2</b> Tiêu chí, ký lúc 14:30–14:35</td><td><code>acceptance_criteria.json</code> + <code>.lock</code> đã push</td><td>A</td></tr>
    <tr><td class="num">14:35</td><td><b>CP3</b> Đo, rủi ro, cổng vòng 1, v1</td><td>Mã lần chạy base, bản chốt vòng 1, v1 đã push</td><td>B</td></tr>
    <tr><td class="num">15:35</td><td><b>CP4</b> Sự cố S1–S8</td><td>Report ba mốc, <code>monitor ✅</code>, <code>regression ✅</code></td><td>C</td></tr>
    <tr><td class="num">16:35</td><td><b>CP5</b> v2, demo, nộp</td><td>Lệnh 7 in <code>ĐỦ THÀNH PHẦN</code></td><td>C12</td></tr>
  </tbody>
</table>
<p class="note">Nghỉ 15:25–15:35. Đẩy bài lần cuối trước 17:30. Hạn nộp link LMS: {{DEADLINE}}.</p>
""",
    """
<strong>Điều phối thời gian</strong>
<ul>
  <li>Lab ghi theo phút 0–240; deck quy về giờ lớp chiều (phút 0 = 13:30). Lớp sáng dời sớm 5 tiếng, deck tự đổi theo giờ máy lúc mở (trước 13:00 là lớp sáng), có nút đổi tay trên header.</li>
  <li>Mốc cứng nhất: <b>ký tiêu chí 14:30–14:35, trước khi chạy đánh giá lần nào</b>. Nhóm nào chạy <code>eval</code> trước khi ký sẽ bị từ chối; nhóm nào ký mà không push ngay thì lịch sử git không chứng minh được.</li>
  <li>Mốc cứng thứ hai: chốt cổng vòng 1 (lệnh 5) trong 15:15–15:25. Không chốt thì không có mốc prepared.</li>
  <li>Phát thẻ lúc 15:35 trên repo mẫu; bàn kéo về bằng <code>git pull … upstream main</code>.</li>
</ul>
""",
)

# 4 ── Repo naming ───────────────────────────────────────────────────────
slide(
    "Tạo repo của bàn và đặt tên",
    """
<h2 class="title">Tạo repo của bàn và đặt tên đúng ngay từ đầu</h2>
<div class="grid grid-2">
  <section class="panel">
    <h3>Tên repo của bàn</h3>
<pre class="code code--wrap">K5_Day10_3A_TenNhom
K5_Day10_3B_TenNhom</pre>
    <p><code>TenNhom</code> không dấu, không khoảng trắng, không thêm chữ <code>Lop</code>. Giá trị <code>team</code> trong tiêu chí và <code>submission.json</code> phải giống hệt tên repo.</p>
    <h3>Gắn repo mẫu</h3>
<pre class="code code--wrap">git remote add upstream https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student.git
git remote -v</pre>
  </section>
  <div class="stack">
    <section class="panel">
      <h3>Danh tính Git</h3>
<pre class="code">git config user.name "&lt;MSSV trưởng nhóm&gt;"
git config user.email "&lt;MSSV&gt;@example.com"</pre>
      <p>Muốn repo Private thì dùng <b>Use this template</b>, không Fork.</p>
    </section>
    <section class="anti">
      <h3>{ICONS_ANTI}Lỗi thường gặp</h3>
      <ul>
        <li>Quên mời tài khoản team chấm quyền Read.</li>
        <li>Không gắn <code>upstream</code>, 15:35 không kéo được thẻ.</li>
        <li>Push nhầm lên repo mẫu.</li>
      </ul>
    </section>
  </div>
</div>
""",
    """
<strong>Hành động của giảng viên trong 15 phút đầu</strong>
<ul>
  <li>Quy ước lấy từ SUBMISSION.md của lab. Tên <code>K5_Day10_&lt;3A|3B&gt;_&lt;TenNhom&gt;</code> giữ nguyên vì lệnh gom bài <code>lab10/check_submission.py</code> (file bị khoá) và team chấm tự động dùng đúng dạng này.</li>
  <li>Trưởng nhóm vào Settings → Collaborators mời tài khoản team chấm (hỏi Lab Coach tên tài khoản) và các bạn trong bàn.</li>
  <li>Email Git là địa chỉ giả <code>&lt;MSSV&gt;@example.com</code>, không dùng email cá nhân.</li>
  <li>Đi một vòng kiểm <code>git remote -v</code> của từng bàn: phải có <code>origin</code> (repo bàn) và <code>upstream</code> (repo mẫu).</li>
</ul>
""",
)

# 5 ── Rules ─────────────────────────────────────────────────────────────
slide(
    "Luật làm bài và ranh giới",
    """
<h2 class="title">Luật làm bài: được làm gì, cấm gì</h2>
<table class="data">
  <thead><tr><th>Phần</th><th>Cách làm đúng</th><th>Hành vi bị cấm</th></tr></thead>
  <tbody>
    <tr><td class="num">Tiêu chí</td><td>Ký một lần, commit và push ngay</td><td>Chạy <code>eval</code> trước khi ký; sửa sau khi ký</td></tr>
    <tr><td class="num">Bản chốt</td><td>Sửa tiếp <code>guards.py</code> và config gốc ở vòng 2</td><td>Sửa <code>guards_round1.py</code>, <code>*.round1.json</code>, <code>round1.lock</code></td></tr>
    <tr><td class="num">Test ẩn</td><td>Cổng tổng quát theo dữ liệu thật</td><td>Xử lý riêng theo mã ticket hay câu chữ</td></tr>
    <tr><td class="num">Ca đang đúng</td><td>Giữ đúng sau khi sửa</td><td>Chặn hết, phạm vi về 0, xếp quá nhiều người</td></tr>
    <tr><td class="num">Thẻ sự cố</td><td>Chỉ làm đúng thẻ đã bốc</td><td>Mở hay tiết lộ thẻ bàn khác</td></tr>
    <tr><td class="num">Dùng AI</td><td>Đọc code, gợi ý cổng, soát câu chữ</td><td>Không giải thích được con số khi demo</td></tr>
  </tbody>
</table>
<p class="note">File bị khoá bằng hash: sửa là lệnh tự kiểm tra báo <code>integrity</code> hỏng.</p>
""",
    """
<strong>Nhấn mạnh với lớp (README mục 5 và RULES.md)</strong>
<ul>
  <li>Đừng mở rồi lưu lại <code>config/acceptance_criteria.json</code> bằng trình soạn thảo tự định dạng: một dấu cách cũng làm đổi hash.</li>
  <li>Ba file bản chốt vòng 1 do lệnh 5 tạo ra; trước 15:15 chưa có là đúng.</li>
  <li>Mọi ngưỡng, con số trong <code>operating_gates.json</code> và quyết định v1/v2 là của bàn; AI gợi ý được nhưng bàn phải giải thích được khi bị phản biện.</li>
  <li>Không commit API key, mật khẩu, file <code>.env</code> (lab không cần key).</li>
</ul>
""",
)

# 6 ── CP1 ───────────────────────────────────────────────────────────────
slide(
    "CP1: Cài đặt và chia vai",
    f"""
<h2 class="title">CP1: repo chạy được, mỗi người một vai</h2>
{meta(when="13:30–13:45", who="Cả bàn", write="<code>TEAM.md</code>", out="Repo của bàn, <code>origin</code> + <code>upstream</code>, test xanh")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap">git clone https://github.com/&lt;trưởng-nhóm&gt;/K5_Day10_3A_XXX.git
cd K5_Day10_3A_XXX
git remote add upstream https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student.git
python3 -m unittest discover -s tests</pre>
    <section class="panel">
      <h3>Chuẩn bị</h3>
      <p>Python 3 và Git. Không cần gói, tài khoản hay khoá API. Đã chạy thử trên Python 3.9.6 và 3.15.</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "<b>Chọn bản chung từ Lab 9:</b> một eval card và một PRD v1.1 làm đầu vào cho cả bàn.",
        "<b>Chia ba vai ngay:</b> Kỹ sư cổng, Sản phẩm và kinh doanh, Vận hành và pháp lý; ghi vai vào <code>TEAM.md</code>.",
        "<b>Windows:</b> thử <code>python</code> nếu <code>python3</code> không chạy.",
    )}
    {anti(
        "Để một người làm hết, ba người ngồi xem.",
        "Bỏ qua bước gắn <code>upstream</code>.",
    )}
    {check("Thấy <code>Ran 13 tests</code> và <code>OK</code>; <code>git remote -v</code> có cả <code>origin</code> và <code>upstream</code>?")}
  </div>
</div>
""",
    """
<strong>Hành động của giảng viên trong CP1</strong>
<ul>
  <li>Cần mạng ở bốn lúc: tạo và clone repo, push tiêu chí đã ký, kéo thẻ lúc 15:35, push bài nộp. Nhắc bàn kiểm wifi từ đầu.</li>
  <li>Lỗi cài đặt: chỉ bàn mở <code>docs/guide.md</code> mục FAQ và Cài đặt.</li>
  <li>Bàn nào xong sớm: đọc tình huống LogiX-VN ở <code>problem-set.md</code> Phần A và mở <code>data/world.json</code> mục <code>staff</code>, <code>ops_limits</code>, <code>ops_facts</code>.</li>
</ul>
""",
    cp="1",
    minutes=15,
    label="CP1 · Cài đặt",
)

# 7 ── CP2 ───────────────────────────────────────────────────────────────
slide(
    "CP2: Tiêu chí, rồi ký",
    f"""
<h2 class="title">CP2: viết tiêu chí, ký trước khi chạy đánh giá</h2>
{meta(when="13:45–14:35", who="Sản phẩm và kinh doanh cầm bút", write="Phiếu A, <code>config/acceptance_criteria.json</code>", out="Tiêu chí đã ký và push")}
<div class="cp-layout">
  <div class="stack">
    <section class="panel">
      <h3>Câu 1.1–1.6 (13:45–14:30) · chưa chạy trợ lý</h3>
      <p>Mục tiêu hệ thống; mục tiêu của chị Oanh (kế toán đối soát) và chị Hạnh (trưởng ca CSKH); một offline metric; telemetry production; khoảng tin cậy; câu “Nếu … thì chúng tôi sẽ …”.</p>
    </section>
<pre class="code"><span class="c"># 14:30–14:35, ngay khi điền xong</span>
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json \\
        config/acceptance_criteria.lock
git commit -m 'Sign acceptance criteria'
git push -u origin main</pre>
  </div>
  <div class="stack">
    {coach(
        "<b>Điền đủ trường:</b> <code>team</code> (= tên repo), <code>signed_by</code>, 5 ngưỡng <code>required</code>, <code>nice_to_have</code>, nhóm <code>business_ops</code> (chi phí mỗi ticket, ROI, số ca ùn), <code>stop_condition</code>, bốn dòng <code>decision_rule</code>.",
        "<b>Không chép ngưỡng từ file example:</b> <code>acceptance_criteria.example.json</code> chỉ để xem cách viết; con số lấy từ <code>data/world.json</code> mục <code>ops_facts</code>.",
        "<b>Chỉ số an toàn có thể để 0:</b> hoàn tiền sai, lỗi oan cho hãng, lộ dữ liệu cá nhân.",
    )}
    {anti(
        "Chạy <code>eval</code> “xem thử” trước khi ký.",
        "Ký xong không push ngay.",
    )}
    {check("Máy in <code>ĐÃ KÝ.</code> và commit ký đã lên GitHub; Phiếu A mục A5 có giờ ký và mã commit?")}
  </div>
</div>
""",
    """
<strong>Vì sao phải ký trước</strong>
<ul>
  <li>Ngưỡng phải được viết khi chưa ai biết trợ lý đạt hay trượt. <code>eval</code> và <code>grade</code> từ chối chạy khi bàn chưa ký.</li>
  <li>Câu 1.6 còn yêu cầu hai câu ranh giới đầu ra (không thêm trường JSON): một đầu ra hoặc hành động bị cấm, một ngưỡng chuyển cho người duyệt.</li>
  <li>Bốn câu soát: có ý nghĩa với mọi bên? ai thiệt? ngày 1? ngày 1.000?</li>
  <li>Lỗi hay gặp: <code>Chưa ký được: thiếu team hoặc ngưỡng bắt buộc</code>, tức còn <code>null</code> trong <code>required</code>.</li>
</ul>
""",
    cp="2",
    minutes=50,
    label="CP2 · Tiêu chí",
    done=1,
)

# 8 ── Three stages ──────────────────────────────────────────────────────
slide(
    "Ba mốc đo: base, prepared, after",
    """
<h2 class="title">Ba mốc đo cho cùng một bộ ticket</h2>
<div class="grid grid-3">
  <section class="panel"><h3>base</h3><p>Bỏ qua mọi cổng của bàn. Trợ lý như PoC.</p><p class="cp-ref">Đo ở CP3, câu 2.1</p></section>
  <section class="panel"><h3>prepared</h3><p>Chỉ cổng vòng 1 đã chốt bằng lệnh 5, trước khi biết sự cố.</p><p class="cp-ref">Đo ngay khi bốc thẻ, câu 3.0</p></section>
  <section class="panel"><h3>after</h3><p>Cổng hiện tại, sau khi bàn sửa ở vòng 2.</p><p class="cp-ref">Đo sau khi sửa, câu 3.5</p></section>
</div>
<table class="data data--compact">
  <thead><tr><th>Report có gì</th><th>Đọc để làm gì</th></tr></thead>
  <tbody>
    <tr><td><code>pass_rate</code>, <code>pass_k</code> (pass^k: đúng cả 5/5 seed)</td><td>So với ngưỡng đã ký</td></tr>
    <tr><td>Kinh doanh và vận hành: chờ duyệt, ca ùn, chi phí mỗi ticket, ROI, tiền hoàn so với trần</td><td>Có dòng nào vượt trần</td></tr>
    <tr><td>Theo kho và hãng</td><td>Phạm vi pilot có nên thu hẹp</td></tr>
  </tbody>
</table>
""",
    """
<strong>Giải thích ba mốc</strong>
<ul>
  <li>Bộ nền: 22 ticket × 5 seed. <code>pass_k</code> ở đây là pass^k, khắt khe hơn <code>pass_rate</code>, khác <code>pass@k</code> (chỉ cần đúng ít nhất một lần).</li>
  <li>Demo cuối buổi chiếu đúng ba cột này: cổng chuẩn bị trước đỡ được gì, phần nào phải sửa sau.</li>
  <li>Dòng kết của report: “được phép cân nhắc Tiếp tục” hay “không đủ căn cứ”. Kết luận tự kiểm tra (<code>FAIL</code>, <code>PARTIAL</code>, <code>PASS-VISIBLE</code>) nói phần sửa tới đâu; nó không bắt bàn phải chọn Tiếp tục.</li>
</ul>
""",
    done=2,
)

# 9 ── CP3 ───────────────────────────────────────────────────────────────
slide(
    "CP3: Đo, tìm rủi ro, dựng cổng vòng 1",
    f"""
<h2 class="title">CP3: đo base, tìm rủi ro, dựng cổng vòng 1</h2>
{meta(when="14:35–15:25", who="Ba vai song song", write="Phiếu B mục B0–B8", out="Mã lần chạy base, 2–3 cổng, cổng config, v1")}
<div class="cp-layout">
  <div class="stack">
<pre class="code code--wrap"><span class="c"># 2A · 14:35–14:55, chưa sửa code hay config</span>
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/&lt;mã&gt;/report.json
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
<span class="c"># 2B · 14:55–15:15, cổng phòng ngừa</span>
python3 -m lab10.eval --suite base --stage after --note "cổng v1"</pre>
    <section class="panel">
      <h3>Song song ở 2A</h3>
      <p>Kỹ sư cổng: câu 2.1–2.2. Kinh doanh: bản đồ dữ liệu, ví dụ drift (2.3). Vận hành: HAZOP ≥ 3 dòng + ≥ 2 dòng ngoài kỹ thuật, checklist 9 nhóm có PIC (2.4). Cả bàn: pre-mortem bốn lăng kính (2.5).</p>
    </section>
  </div>
  <div class="stack">
    {coach(
        "<b>Cổng nào cũng trỏ về một rủi ro:</b> mỗi cổng trong <code>pre_guard</code> hoặc <code>write_gate</code> ứng với một lý do pre-mortem hoặc một dòng HAZOP.",
        "<b>Cổng không cần code:</b> trần tiền hoàn mỗi ngày, ngân sách mỗi ticket, phạm vi pilot, người trực, thời gian chờ tối đa nằm trong <code>config/operating_gates.json</code>.",
        "<b>Viết một behavioral test:</b> 2 ticket mới chạy bằng <code>--adhoc</code>; giữ làm “ticket hiểm” cho demo (câu 2.8).",
    )}
    {anti(
        "Chỉnh cổng tới khi 22 ticket xanh hết (rò rỉ dữ liệu).",
        "Cổng làm hỏng ticket đang đúng của bộ nền.",
    )}
    {check("<code>T-002@55</code> đã xếp loại lỗi? Pre-mortem đủ bốn lăng kính? Test công khai vẫn xanh?")}
  </div>
</div>
""",
    """
<strong>Hành động của giảng viên trong CP3</strong>
<ul>
  <li>Câu 2.1 còn hỏi: để cổng so tiêu chí tự chặn bản phát hành hay để người duyệt? Yêu cầu bàn khoanh khuyến nghị và nêu lý lẽ hai phía.</li>
  <li>Câu 2.7: bàn nêu 2 bước tránh rò rỉ dữ liệu, gắn với bộ nền, gói sự cố và bài kiểm tra ẩn.</li>
  <li>Câu 2.10: runbook phần 1–3 phải khớp con số trong config, kể cả thời hạn dừng (từ tín hiệu đỏ đến lúc dừng xong tối đa bao nhiêu phút, ai bấm) và mục Giờ cao điểm.</li>
  <li>Ví dụ viết cổng: <code>docs/guide.md</code> Phụ lục C; hàm tra cứu trong <code>lab10/helpers.py</code>.</li>
</ul>
""",
    cp="3",
    minutes=50,
    label="CP3 · Rủi ro và cổng",
    done=2,
)

# 10 ── Lock round 1 ─────────────────────────────────────────────────────
slide(
    "Chốt vòng 1 và quyết định v1",
    """
<h2 class="title">15:15–15:25: chốt cổng vòng 1, quyết định v1</h2>
<ol class="loop loop--three">
  <li><b>Chốt cổng</b><span><code>python3 -m lab10.checkpoint</code> chụp <code>guards.py</code> và <code>operating_gates.json</code> thành mốc prepared.</span></li>
  <li><b>Đo prepared, so tiêu chí</b><span><code>eval --suite base --stage prepared</code> rồi <code>gate --run …</code>.</span></li>
  <li><b>Điền v1, push</b><span>Phiếu B mục B8: quyết định, ba dòng bằng chứng có mã lần chạy, dòng <code>decision_rule</code>.</span></li>
</ol>
<div class="grid grid-2">
  <section class="panel"><h3>Ba câu tự vấn</h3><p>Rủi ro còn lại chấp nhận được như hiện trạng? Cần thêm biện pháp nào, tốn bao lâu? Có phần nào không nên làm tiếp?</p></section>
  <section class="anti"><h3>{ICONS_ANTI}Sau mốc này</h3><ul><li>v1 không sửa được nữa.</li><li>Không sửa hai bản chụp vòng 1.</li></ul></section>
</div>
""",
    """
<strong>Chuyển pha</strong>
<ul>
  <li>Báo lớp 10 phút trước 15:15. Bàn nào chưa chốt sẽ không có mốc prepared, và lệnh 7 cuối buổi sẽ báo thiếu.</li>
  <li>Tiêu chí đã ký từ 14:30–14:35; ở đây không ký lại.</li>
  <li>Nhắc commit và push xong mới đi nghỉ.</li>
</ul>
""",
    done=3,
)

# 11 ── Incident drop ────────────────────────────────────────────────────
slide(
    "Phát thẻ sự cố",
    """
<h2 class="title">15:35: phát thẻ sự cố S1–S8</h2>
<pre class="code code--wrap">git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main
python3 -m lab10.grade --incident Sx   <span class="c"># trước khi sửa bất cứ thứ gì</span></pre>
<div class="grid grid-2">
  <section class="panel">
    <h3>Mỗi cặp bàn bốc một số</h3>
    <p>Hai bàn trong cặp làm cùng thẻ. Mở <code>incidents/Sx/card.md</code>, ghi số vào dòng <code>Thẻ đã bốc:</code> ở đầu Phiếu C.</p>
  </section>
  <section class="panel">
    <h3>Tám thẻ, tám tác hại</h3>
    <p>Năm thẻ nguyên nhân chính ở kỹ thuật. Ba thẻ ở kinh doanh hoặc con người: hàng chờ ngập, chi phí cao hơn làm tay, nhân viên không tin trợ lý.</p>
  </section>
</div>
<p class="note">“Đây là tin nhắn bàn nhận được sáng nay. Bản tiêu chí đã ký giữ nguyên. Sau 60 phút, bàn cho tôi biết quyết định Gate 1 còn đứng được không.”</p>
""",
    """
<strong>Kịch bản phát thẻ</strong>
<ul>
  <li>Đẩy thẻ lên repo mẫu, rồi báo “đã phát”. Bàn kéo trước giờ sẽ thấy <code>Already up to date</code>: chờ rồi kéo lại.</li>
  <li><code>'upstream' does not appear to be a git repository</code>: gắn lại bằng bước 2a. <code>Please tell me who you are</code>: làm bước 2b. Xung đột: <code>git merge --abort</code> rồi chạy lại đủ lệnh.</li>
  <li>Kéo đúng thì report có <code>1 integrity | ✅</code>. Lab Coach ghi số thẻ của từng cặp vào sổ.</li>
  <li>Ở thẻ kinh doanh hoặc con người, cách sửa nằm nhiều ở phạm vi, nhân sự, giải thích, quy trình hơn là ở code.</li>
</ul>
""",
    done=3,
)

# 12 ── CP4 ──────────────────────────────────────────────────────────────
slide(
    "CP4: Sự cố, phân tích và sửa",
    f"""
<h2 class="title">CP4: một tác hại cụ thể, nhiều nguyên nhân</h2>
{meta(when="15:35–16:35", who="Cả bàn", write="Phiếu C mục C0–C11", out="Report ba mốc, chỉ số theo dõi mới")}
<div class="cp-layout">
  <div class="stack">
<table class="data data--compact">
  <thead><tr><th>Giờ</th><th>Việc</th></tr></thead>
  <tbody>
    <tr><td class="num">15:35</td><td>3.0 Mốc prepared: cổng vòng 1 đỡ được ô nào</td></tr>
    <tr><td class="num">15:45</td><td>3.1–3.4 Trace ≥ 2 ticket, HAZOP của thẻ, spec, giả định môi trường, fault tree</td></tr>
    <tr><td class="num">16:05</td><td>3.5–3.6 Sửa đúng chỗ; thêm hàm vào <code>MONITORS</code></td></tr>
    <tr><td class="num">16:30</td><td>3.7 Fault tree sau sửa, risk register, runbook 4–5</td></tr>
  </tbody>
</table>
<pre class="code">python3 -m lab10.trace --suite Sx --ticket &lt;ID&gt; --seed 11
python3 -m lab10.eval --suite Sx --stage after --note "…"
python3 -m lab10.grade --incident Sx</pre>
  </div>
  <div class="stack">
    {coach(
        "<b>Tác hại cho ai, đo bằng gì:</b> nêu bên chịu hại và con số ở mốc base trước khi sửa.",
        "<b>Fault tree có hai tầng:</b> ít nhất hai nhánh ở hai tầng khác nhau (kỹ thuật, kinh doanh, con người), mỗi lá có bằng chứng <code>ticket@seed</code> hoặc một dòng report.",
        "<b>Giảm hay ngăn:</b> mỗi biện pháp ghi rõ chỉ giảm khả năng hay ngăn hẳn tác hại.",
    )}
    {anti(
        "Sửa ngay khi chưa chạy mốc prepared.",
        "Thẻ con người mà chỉ sửa code.",
        "Ghi đè HAZOP vòng 1.",
    )}
    {check("Report có <code>monitor ✅</code> và <code>regression ✅</code>? Còn vượt trần nào không?")}
  </div>
</div>
""",
    """
<strong>Hành động của giảng viên trong CP4</strong>
<ul>
  <li>Bảng soát lỗi cần ≥ 2 lỗi có nguồn khác nhau và ≥ 1 lỗi chìm. Phần riêng của thẻ (mục C3) do Vận hành và pháp lý cầm bút.</li>
  <li>Sửa có ba chỗ: code (<code>lab10/guards.py</code>), con số và quy trình (<code>config/operating_gates.json</code>: phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý), và người.</li>
  <li>Chỉ số theo dõi mới có thể là kỹ thuật, vận hành hay kinh doanh; viết đủ ba ô thước đo → dữ liệu → cách tính (mục C8).</li>
  <li>Report tự kiểm tra có sáu mục: file khoá, tiêu chí, gói sự cố, test ẩn (máy bàn hiện “—”), bộ nền, chỉ số theo dõi.</li>
</ul>
""",
    cp="4",
    minutes=60,
    label="CP4 · Sự cố",
    done=3,
)

# 13 ── Decisions ────────────────────────────────────────────────────────
slide(
    "Bốn quyết định Gate 1",
    """
<h2 class="title">Quyết định v2: cái nào cũng đạt nếu khớp bằng chứng</h2>
<table class="data">
  <thead><tr><th>Quyết định</th><th>Đạt khi</th><th>Không đạt khi</th></tr></thead>
  <tbody>
    <tr><td class="num">Tiếp tục</td><td>Mọi ngưỡng đã ký đạt, không dòng nào vượt trần</td><td>Report còn vượt trần hoặc ngưỡng chưa đạt</td></tr>
    <tr><td class="num">Thu hẹp</td><td>Ghi rõ cắt kho nào, còn bao nhiêu phần trăm, mấy người trực, ticket bị cắt đi đâu</td><td>Thu hẹp về 0 để né số</td></tr>
    <tr><td class="num">Cải tiến thêm</td><td>Giả thuyết cụ thể, có hạn</td><td>“Cần thêm thời gian” chung chung</td></tr>
    <tr><td class="num">Dừng</td><td>Có lý do, có số, bài học ghi lại</td><td>Dừng mà không chỉ ra con số nào</td></tr>
  </tbody>
</table>
<h3 class="sub">Ba dòng bắt buộc (Phiếu C mục C12, chép vào <code>submission.json</code>)</h3>
<ol class="loop loop--three">
  <li><b>Giả định môi trường</b><span>Thiết kế đang dựa vào, có thể sai ngoài thực tế.</span></li>
  <li><b>Giảm hay ngăn</b><span>Cổng chỉ giảm khả năng hay ngăn hẳn, vì sao.</span></li>
  <li><b>Đo lại trong pilot</b><span>Data là mock: cần đo gì trước Gate 2.</span></li>
</ol>
""",
    """
<strong>Điều kiện qua</strong>
<ul>
  <li>Quyết định phải khớp bằng chứng và khớp tiêu chí đã ký. Đây là điều kiện để bài được tính, không phải một tiêu chí cộng điểm.</li>
  <li>Cột v2 còn ghi: đổi hay giữ so với v1 và vì con số nào, mã lần chạy của ba mốc.</li>
  <li>Hỏi soi khi đi vòng: “con số nào trong report đỡ cho quyết định này?”</li>
</ul>
""",
    done=4,
)

# 14 ── CP5 ──────────────────────────────────────────────────────────────
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
    <tr><td class="num">16:35</td><td>v2, <code>submission.json</code>, lệnh 7 tới khi đủ</td></tr>
    <tr class="row-key"><td class="num">16:50</td><td>Demo: hai bàn cùng thẻ ghép cặp, mỗi bàn 5 phút; 2–3 bàn lên trước lớp</td></tr>
    <tr><td class="num">17:20</td><td>Trả số về bản v2, chạy lại lệnh 6 và 7, push</td></tr>
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
        "<b>Demo chiếu ba cột:</b> base · prepared · after; cổng vòng 1 đỡ được gì, phần sửa là code, con số hay người.",
        "<b>Bàn kia phản biện:</b> đưa ticket hiểm (câu 2.8) chạy bằng <code>--adhoc</code>, hoặc đổi một con số trong <code>operating_gates.json</code> rồi chạy lại.",
        "<b>members có MSSV:</b> ghi dạng <code>&quot;HoVaTen-MSSV&quot;</code>, khớp <code>TEAM.md</code>.",
    )}
    {anti(
        "Quên trả con số demo về bản v2 trước khi gom.",
        "Chỉ trưởng nhóm nộp link LMS.",
    )}
    {check("Lệnh 7 in <code>ĐỦ THÀNH PHẦN</code> trên đúng code và config cuối cùng?")}
  </div>
</div>
""",
    """
<strong>Hành động của giảng viên trong CP5</strong>
<ul>
  <li>Nếu sau demo bàn không chạy lại lệnh 6, lệnh 7 sẽ báo “báo cáo không chạy trên đúng code và config hiện tại”.</li>
  <li>Lab Coach hỏi soi theo phiếu thẻ, không cho điểm. Ghi nhận câu trả lời demo cho người đọc ở team chấm.</li>
  <li>Cuối buổi: mỗi người viết exit ticket trong mục cá nhân của <code>TEAM.md</code> và tự nộp link repo trên LMS.</li>
  <li>Không push lên repo mẫu (<code>upstream</code>).</li>
</ul>
""",
    cp="5",
    minutes=55,
    label="CP5 · v2 và nộp",
    done=4,
)

# 15 ── Seven commands ───────────────────────────────────────────────────
slide(
    "Bảy lệnh của lab",
    """
<h2 class="title">Bảy lệnh, dùng khi nào</h2>
<table class="data data--compact">
  <thead><tr><th>#</th><th>Lệnh</th><th>Dùng khi</th></tr></thead>
  <tbody>
    <tr><td class="num">1</td><td><code>python3 -m lab10.criteria sign</code></td><td>Ký tiêu chí, một lần, 14:30–14:35</td></tr>
    <tr><td class="num">2</td><td><code>python3 -m lab10.eval --suite … --stage … --note "…"</code></td><td>Chạy trợ lý trên một bộ ticket, in mã lần chạy</td></tr>
    <tr><td class="num">3</td><td><code>python3 -m lab10.trace --suite … --ticket … --seed …</code></td><td>Xem từng bước với một ticket, hoặc <code>--adhoc</code></td></tr>
    <tr><td class="num">4</td><td><code>python3 -m lab10.gate --run runs/&lt;mã&gt;/report.json</code></td><td>So một lần chạy với tiêu chí đã ký</td></tr>
    <tr><td class="num">5</td><td><code>python3 -m lab10.checkpoint</code></td><td>Chốt cổng vòng 1, một lần, 15:15–15:25</td></tr>
    <tr><td class="num">6</td><td><code>python3 -m lab10.grade --incident Sx</code></td><td>Tự kiểm tra trên thẻ ở ba mốc, từ 15:35</td></tr>
    <tr><td class="num">7</td><td><code>python3 -m lab10.check_submission --collect</code></td><td>Gom bài nộp, kiểm đủ thành phần</td></tr>
  </tbody>
</table>
""",
    """
<strong>Tra cứu</strong>
<ul>
  <li>Output mẫu và cách đọc từng dòng: <code>docs/guide.md</code> Phụ lục A–B và mục “Các mẫu kết quả đầy đủ”.</li>
  <li>Seed hợp lệ cho trace: 11, 22, 33, 44, 55.</li>
  <li>Khi lệnh có <code>&lt;mã lần chạy&gt;</code>, thay cả dấu ngoặc nhọn bằng mã vừa in ra.</li>
</ul>
""",
    done=4,
)

# 16 ── Rubric ───────────────────────────────────────────────────────────
RUBRIC_ROWS = [
    ("C1", "Tiêu chí và cách đo (Phiếu A)", "CP2", 15),
    ("C2", "Rủi ro trước sự cố", "CP3", 15),
    ("C3", "Cổng vòng 1 và quyết định v1", "CP3", 15),
    ("C4", "Máy đo trên thẻ và test ẩn", "CP4", 25),
    ("C5", "Phân tích và sửa sự cố", "CP4", 20),
    ("C6", "Quyết định v2 và ba dòng", "CP5", 10),
]
_rubric = "\n".join(
    f'      <tr><td><b>{c}</b> {name}</td><td>{cp}</td><td class="bar-cell" title="{pts} điểm"><span class="bar" style="--v: {pts / 25:.3f}"></span><span class="bar-val">{pts}</span></td></tr>'
    for c, name, cp, pts in RUBRIC_ROWS
)
slide(
    "Rubric: 100 điểm chính, C1 đến C6",
    f"""
<h2 class="title">Rubric: 100 điểm chính, C1 đến C6</h2>
<div class="grid grid-rubric">
  <table class="data data--compact">
    <thead><tr><th>Tiêu chí</th><th>Checkpoint</th><th>Điểm</th></tr></thead>
    <tbody>
{_rubric}
    </tbody>
  </table>
  <div class="stack">
    <section class="anti">
      <h3>{{ICONS_ANTI}}Không qua nếu</h3>
      <ul>
        <li>Ký sau khi đã đo, hoặc sửa sau khi ký.</li>
        <li>File khoá hay bản chốt bị sửa.</li>
        <li>Quyết định không khớp bằng chứng.</li>
        <li>Lệnh 7 chưa <code>ĐỦ THÀNH PHẦN</code>.</li>
      </ul>
    </section>
    <p class="note">Bonus tối đa +10, ghi riêng.</p>
  </div>
</div>
""",
    """
<strong>Quy tắc chấm (RUBRIC.md, bản đề xuất trong PR #1, chờ giảng viên duyệt)</strong>
<ul>
  <li>Ba lớp chấm theo <code>problem-set.md</code> phần D: phần máy đo (test ẩn, chỉ số kinh doanh và vận hành, mức chuẩn bị ở prepared, hash, không làm hỏng ca đúng), phần người đọc (pre-mortem, HAZOP, checklist có PIC, runbook, Phiếu C, ba dòng, câu trả lời demo), và điều kiện qua.</li>
  <li>Bonus: cổng vòng 1 đỡ được phần lớn sự cố (+5); chỉ số hoặc cổng bắt được lỗi chìm ngoài thẻ, có trace (+5).</li>
  <li>Trừ chung: thiếu mục cá nhân trong <code>TEAM.md</code>; <code>members</code> thiếu MSSV (−5); sai tên repo hoặc <code>team</code> không khớp (−5).</li>
  <li>Nếu trọng số chính thức khác, sửa <code>RUBRIC_ROWS</code> trong <code>content/build_content.py</code> rồi build lại.</li>
</ul>
""",
    done=5,
)

# 17 ── Submit checklist ─────────────────────────────────────────────────
slide(
    "Checklist nộp bài và khởi động lab",
    """
<h2 class="title">Checklist nộp bài và khởi động lab</h2>
<div class="grid grid-2">
  <div>
    <h3 class="sub">Trước khi nộp</h3>
    <ul class="checklist">
      <li>Tên repo <code>K5_Day10_3A_…</code> hoặc <code>K5_Day10_3B_…</code>, đã mời team chấm</li>
      <li><code>TEAM.md</code> đủ họ tên, MSSV, vai và mục cá nhân từng người</li>
      <li>Tiêu chí ký và push trước lần đo đầu tiên</li>
      <li>Đã chốt vòng 1; ba phiếu A, B, C đã điền</li>
      <li><code>submission.json</code> đủ trường, <code>members</code> có MSSV</li>
      <li>Lệnh 7 in <code>ĐỦ THÀNH PHẦN</code></li>
      <li>Không có <code>.env</code> hay key</li>
      <li>Mọi thành viên nộp link trên LMS</li>
    </ul>
  </div>
  <div class="stack">
    <section class="panel">
      <h3>Deadline (GMT+7)</h3>
      <p class="deadline">{{DEADLINE}}</p>
      <p>Đẩy bài trong buổi trước 17:30. Coach có thể gia hạn tối đa 48h.</p>
    </section>
    <div class="cta-row">
      <button class="btn-primary" type="button" onclick="window.kickoffLab && window.kickoffLab()">Bắt đầu CP1: Cài đặt</button>
    </div>
  </div>
</div>
""",
    """
<strong>Lời dặn kết thúc</strong>
<ul>
  <li>Bấm nút để quay về CP1 và bắt đầu.</li>
  <li>Deadline (GMT+7) theo ca: lớp sáng 23h59 ngày lab, lớp chiều 11h59 sáng hôm sau. Slide tự hiện đúng mốc của ca đang mở.</li>
  <li>Commit sau hạn chót không được tính; team chấm lấy commit cuối trước hạn.</li>
  <li>Lỗi kỹ thuật sau buổi: gửi mô tả lỗi kèm ảnh chụp lệnh và output trước deadline.</li>
</ul>
""",
    done=5,
)

out = pathlib.Path(__file__).resolve().parent.parent / "app/src/slides/content.json"
out.write_text(json.dumps(S, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {len(S)} slides -> {out}")
