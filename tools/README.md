# Day 10: quay thẻ và tải thẻ

Hai trang tĩnh, deploy trên GitHub Pages:

| Trang | Ai dùng | URL |
|---|---|---|
| `card-draw/` | Lab Coach, chiếu trên máy chiếu | https://sagitakdx.github.io/k5-day10-card-draw/ |
| `card-pack/site/` | Nhóm trưởng, nhập mã để tải gói thẻ | https://sagitakdx.github.io/k5-day10-cards/ |

## Cách chạy

- Trang quay chia đều 8 thẻ cho các cặp. Hai nhóm cùng cặp luôn cùng thẻ. Nếu số nhóm lẻ, một cặp có 3 nhóm.
- Mỗi lượt quay phát một mã tải thẻ từ file mã của cụm.
- Trang tải nhận mã, giải mã gói zip và tải về.
- Gói zip luôn có **cả 8 thẻ**, vì `lab10.grade` kiểm hash của cả 32 file thẻ.

## Làm lại gói và mã (khi thẻ thay đổi)

1. Dựng gói thẻ bằng `release_incidents.py` của labcoach, trên một bản clone sạch của repo mẫu. Kiểm `integrity` ✅.
2. Nén gói: `zip -X -r the-su-co-day10.zip incidents/S1 … incidents/S8 incident-cards.md`.
3. Mã hoá gói và sinh mã:

   ```bash
   node tools/card-pack/build_pack.mjs the-su-co-day10.zip tools/card-pack/site <thư-mục-mã-bí-mật> 10 16
   ```

4. Deploy lại `tools/card-pack/site/` lên Pages. Mã cũ không còn dùng được.

**WARNING:** Không commit các file `codes-*.csv`. Ai có mã đều tải được gói thẻ.
