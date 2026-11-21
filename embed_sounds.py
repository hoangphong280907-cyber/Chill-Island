# Nhúng thẳng file âm thanh vào index.html (1 file duy nhất, không cần thư mục sounds).
# Cách dùng:  python embed_sounds.py index.html sounds index_co_am_thanh.html
# Lưu ý: dùng index.html GỐC (chưa nhúng). Mỗi file nhúng nặng thêm khoảng 1/3, nên chỉ nhúng file ngắn, nhẹ (mp3, ogg).
import sys, os, re, base64, unicodedata
IDS = set(['bao', 'bien', 'bo', 'bong_nay', 'bw_do', 'bw_lan', 'bw_va', 'chim_hot', 'cho', 'coi_xe', 'cuu', 'dap_bang', 'dong_co', 'dut_day', 'ga', 'gio_bao', 'gio_tuyet', 'hamster', 'heo', 'hw_khach', 'hw_ma', 'hw_ruong', 'keo_ca', 'keo_day', 'luoi', 'meo', 'mo_halloween', 'mo_nye', 'mo_summer', 'mo_tet', 'mo_thattich', 'mo_trungthu', 'mo_xmas', 'mua', 'nem_tieu', 'nhac_nen', 'ny_dem', 'ny_giaothua', 'ny_hop', 'ny_phao', 'ny_xoso', 'quang_day', 'rai_ca', 'reo_bd', 'reo_bw', 'reo_rl', 'sam', 'sk_bong_bay', 'sk_cao', 'sk_duoi', 'sk_hop_qua', 'sk_ket_thuc', 'sk_khi', 'sk_ruong', 'sk_sao_bang', 'sk_thanh_tuu', 'sk_trom', 'song_bien', 'su_boi', 'su_cat', 'su_kem', 'su_party', 'su_quay', 'su_song', 'sut_bong', 'tet_banh', 'tet_chuc', 'tet_duxuan', 'tet_giaothua', 'tet_lixi', 'tet_phao', 'tieu_dam', 'tt_cau', 'tt_dem', 'tt_det', 'tt_ghep', 'tt_sao', 'tt_trau', 'tt_uoc', 'tu_banh', 'tu_den', 'tu_lan', 'tu_ruoc', 'tu_trang', 'vanh_ro', 'xem_boi', 'xm_qua', 'xm_santa', 'xm_treo', 'xm_tuanloc', 'xuc_xac'])
MIME = {".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".wav": "audio/wav", ".m4a": "audio/mp4", ".aac": "audio/aac", ".flac": "audio/flac", ".webm": "audio/webm"}
def slot(name):
    n = os.path.splitext(name)[0].lower()
    n = unicodedata.normalize("NFD", n)
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    n = re.sub(r"[^a-z0-9]+", "_", n).strip("_")
    return n if n in IDS else None
if len(sys.argv) < 4:
    sys.exit("Cách dùng: python embed_sounds.py index.html sounds index_co_am_thanh.html")
html_in, folder, html_out = sys.argv[1], sys.argv[2], sys.argv[3]
html = open(html_in, encoding="utf-8").read()
if "/*SND*/" not in html:
    sys.exit("Không thấy chỗ nhúng /*SND*/ - hãy dùng index.html gốc, chưa nhúng âm thanh.")
items, skipped, total = [], [], 0
for f in sorted(os.listdir(folder)):
    ext = os.path.splitext(f)[1].lower()
    if ext not in MIME:
        continue
    s = slot(f)
    if not s:
        skipped.append(f)
        continue
    b = open(os.path.join(folder, f), "rb").read()
    total += len(b)
    items.append('"' + s + '":"data:' + MIME[ext] + ';base64,' + base64.b64encode(b).decode() + '"')
open(html_out, "w", encoding="utf-8").write(html.replace("/*SND*/", ",".join(items), 1))
print("Đã nhúng", len(items), "file (", round(total / 1048576, 1), "MB gốc ) ->", html_out)
if skipped:
    print("Bỏ qua (sai tên):", ", ".join(skipped))
