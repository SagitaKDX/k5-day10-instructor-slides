# Nội dung deck

- `build_content.py`: HTML và speaker notes của từng slide. Chạy `python3 -I content/build_content.py` từ thư mục gốc để sinh `app/src/slides/content.json`.
- `icons.json`: SVG Lucide dùng trong slide, sinh bằng `node scripts/build_icons.mjs` (chạy trong `app/`).

## Nguồn sự thật

Deck lấy nội dung từ repo lab [VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student](https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student), PR #1 (nhánh `docs/k5-lab-convention`):

- `README.md`, `problem-set.md`: timeline phút 0–240, câu 1.1–3.7, bảy lệnh, luật
- `CHECKPOINTS.md`: 5 checkpoint CP1 đến CP5
- `RUBRIC.md`: 100 điểm C1 đến C6, bonus tối đa 10 (bản đề xuất, chờ duyệt)
- `RULES.md`, `SUBMISSION.md`, `TEAM.md`: AI, liêm chính, tên repo `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1`, deadline GMT+7, nộp LMS cá nhân

Khi repo lab thay đổi, cập nhật `build_content.py` theo các file trên rồi chạy lại.
