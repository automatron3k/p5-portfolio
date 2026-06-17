#!/usr/bin/env python3
"""Escanea sketches/<proyecto>/<nombre>/ y genera manifest.json para la galería.

Uso:  python3 build.py
Corre esto antes de cada commit (o lo corre el deploy en la VM).
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).parent
SKETCHES = ROOT / "sketches"


def main():
    items = []
    for project_dir in sorted(p for p in SKETCHES.iterdir() if p.is_dir()):
        for sketch_dir in sorted(s for s in project_dir.iterdir() if s.is_dir()):
            index = sketch_dir / "index.html"
            if not index.exists():
                continue  # no es un sketch ejecutable
            meta_path = sketch_dir / "meta.json"
            meta = {}
            if meta_path.exists():
                try:
                    meta = json.loads(meta_path.read_text())
                except json.JSONDecodeError as e:
                    print(f"  WARN meta.json inválido en {sketch_dir}: {e}")
            rel = sketch_dir.relative_to(ROOT).as_posix()
            items.append({
                "path": rel + "/",
                "project": project_dir.name,
                "name": sketch_dir.name,
                "title": meta.get("title") or sketch_dir.name,
                "date": meta.get("date", ""),
                "tags": meta.get("tags", []),
                "source": meta.get("source", ""),
                "description": meta.get("description", ""),
            })

    # más nuevos primero (por fecha, luego por nombre)
    items.sort(key=lambda x: (x["date"], x["name"]), reverse=True)
    manifest = {"count": len(items), "sketches": items}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"manifest.json -> {len(items)} sketches")


if __name__ == "__main__":
    main()
