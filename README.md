# K5 Day 10: Instructor Slides (React)

Deck giảng viên **From PoC to Pilot (Gate 1)**, cùng khung với deck Day 02 và Day 03 (Vite + React, timer theo checkpoint, ghi chú giảng viên).

Nội dung lấy từ repo lab `VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student` (PR #1, nhánh `docs/k5-lab-convention`). Logo Vingroup và VinUniversity cắt từ trang https://vinuni.edu.vn/aithucchien/.

## Live

https://sagitakdx.github.io/k5-day10-instructor-slides/ (thêm `?ca=sang` hoặc `?ca=chieu` để chọn ca)

## Sửa nội dung

Nội dung slide nằm trong `content/build_content.py` (HTML của từng slide và speaker notes). Sửa file này rồi sinh lại JSON:

```bash
python3 -I content/build_content.py
```

Thang điểm trên slide Rubric lấy từ `RUBRIC.md` bản đề xuất trong PR #1 của repo lab. Khi trọng số chính thức chốt, sửa `RUBRIC_ROWS` rồi build lại.

## Dev

```bash
cd app
npm install
npm run dev
```

## Build (GitHub Pages subpath)

```bash
cd app
npm run build
# output: app/dist, base path /k5-day10-instructor-slides/
# deploy: copy app/dist/ vào SagitaKDX.github.io/k5-day10-instructor-slides/ rồi push
```

## Lớp sáng và lớp chiều

Lab ghi mốc theo phút 0 đến 240; deck quy về giờ lớp chiều (phút 0 = 13:30) và tự chọn ca theo giờ máy lúc mở trang:

- Mở trước 13:00: **lớp sáng**, 08:30 đến 12:30.
- Mở từ 13:00: **lớp chiều**, 13:30 đến 17:30.

Lớp sáng dùng cùng lịch, dời sớm 5 tiếng: mọi mốc giờ trên slide và trong ghi chú tự đổi, hạn nộp của ca hiện tại được tô đậm. Nút ca trên header đổi tay và ghi vào link (`?ca=sang` hoặc `?ca=chieu`).

Lớp sáng bắt đầu giờ khác thì sửa `MORNING_SHIFT_HOURS` trong `app/src/session.ts`.

## Phím tắt

| Phím | Việc |
|------|------|
| ← → / Space | Đổi slide |
| P / R | Dừng hoặc chạy timer / đặt lại |
| M | Âm báo |
| B | Nhạc nền |
| N | Ghi chú giảng viên |
| F | Toàn màn hình |

Ngôn ngữ slide theo ASD-STE100 áp cho tiếng Việt: câu ngắn, câu lệnh bắt đầu bằng động từ, một từ một nghĩa (xem slide "Từ dùng trong buổi" và ghi chú đầu phần thân `content/build_content.py`).

Timer tự chạy khi mở slide CP1 (15 phút), CP2 (50 phút), CP3 (50 phút), CP4 (60 phút), CP5 (55 phút). Âm báo và nhạc nền mặc định tắt. `prefers-reduced-motion` tắt chuyển động và nhạc.
