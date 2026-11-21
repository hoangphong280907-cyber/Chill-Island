# Tạo sounds/manifest.json (danh sách file âm thanh) cho game.
# Cách dùng: đặt file này cạnh thư mục "sounds", chạy:  python make_manifest.py
import os, json, sys
d = sys.argv[1] if len(sys.argv) > 1 else "sounds"
exts = (".mp3", ".ogg", ".wav", ".m4a", ".aac", ".flac", ".webm")
names = sorted(f for f in os.listdir(d) if f.lower().endswith(exts))
with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(names, f, ensure_ascii=False, indent=1)
print(len(names), "file ->", os.path.join(d, "manifest.json"))
