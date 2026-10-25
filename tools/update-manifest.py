#!/usr/bin/env python3
"""Refresh recipes.json after editing recipes.

Run from the repo root: python3 tools/update-manifest.py
- Recomputes each recipe's sha256.
- If a recipe's file changed, bumps its patch version (1.0.0 -> 1.0.1).
- Adds any new <group>/<id>/SKILL.md folder (description left as TODO: fill it in).
- Drops entries whose folder no longer exists.
"""
import datetime, hashlib, json, pathlib, re

RAW = "https://raw.githubusercontent.com/the-react-native-rewind/grokking-out-recipes/main/"
GROUPS = ["general", "website", "email", "accounting"]
root = pathlib.Path(__file__).resolve().parent.parent
manifest_path = root / "recipes.json"
manifest = json.loads(manifest_path.read_text())
old = {r["id"]: r for r in manifest["recipes"]}

recipes = []
for group in GROUPS:
    for p in sorted((root / group).glob("*/SKILL.md")):
        rid = p.parent.name
        text = p.read_text()
        name = re.search(r"^name: (.*)$", text, re.M).group(1).strip()
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        r = old.get(rid, {"description": "TODO: one line on what this recipe is for", "version": "1.0.0", "sha256": sha})
        version = r["version"]
        if r["sha256"] != sha:
            a, b, c = (int(x) for x in version.split("."))
            version = f"{a}.{b}.{c + 1}"
        rel = p.relative_to(root).as_posix()
        recipes.append({"id": rid, "name": name, "group": group, "path": rel, "url": RAW + rel,
                        "description": r["description"], "version": version, "sha256": sha})

manifest["recipes"] = recipes
manifest["updated"] = datetime.date.today().isoformat()
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
print(f"{len(recipes)} recipes written to recipes.json")
