import json, hashlib, re

words = json.load(open("__JSON_FILE__", encoding="utf-8"))
assert len(words) >= 60  # word list is NOT capped at a fixed count (2026-11 확정 규칙); quiz still draws the first 60

# quiz uses the first 60 words (order of appearance); any extra words beyond that are
# vocabulary-list-only (not quizzed), per the "no fixed count" rule
selected = words[:60]

def normalize(s):
    s = s.strip().lower()
    s = re.sub(r"[\s,./·\-()]", "", s)
    return s

def sha256_hex(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def variants(kdef, ensyn):
    parts = [p.strip() for p in kdef.split(",") if p.strip()]
    parts += [p.strip() for p in ensyn.split(",") if p.strip()]
    return parts

quiz_a = []
quiz_b = []
for i, w in enumerate(selected):
    display = f"{w['kdef']}  ({w['ensyn']})"
    vs = variants(w['kdef'], w['ensyn'])
    hashes = [sha256_hex(normalize(v)) for v in vs]
    item = {"id": 0, "word": w["word"], "hashes": hashes, "display": display}
    if i % 2 == 0:
        quiz_a.append(item)
    else:
        quiz_b.append(item)

for i, item in enumerate(quiz_a, 1):
    item["id"] = i
for i, item in enumerate(quiz_b, 1):
    item["id"] = i

print("A:", len(quiz_a), "B:", len(quiz_b))

json.dump(quiz_a, open("quiz_a_data.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(quiz_b, open("quiz_b_data.json", "w", encoding="utf-8"), ensure_ascii=False)
print("wrote quiz_a_data.json, quiz_b_data.json")
