from pathlib import Path

root = Path(__file__).resolve().parents[1]

index_path = root / "index.html"
index = index_path.read_text(encoding="utf-8")
old_index = "        .brand-panel h1 br { display: none; }\n"
new_index = "        .brand-panel h1 br { display: block; }\n        .brand-panel h1 em { white-space: nowrap; }\n"
if old_index not in index:
    raise SystemExit("index mobile heading marker not found")
index_path.write_text(index.replace(old_index, new_index, 1), encoding="utf-8")

settings_path = root / "settings.html"
settings = settings_path.read_text(encoding="utf-8")
old_settings = "        body > .max-w-3xl > header { top: 8px; }\n"
new_settings = "        body > .max-w-3xl > header { top: 8px; }\n        body > .max-w-3xl > header > a { white-space: nowrap; flex-shrink: 0; font-size: 12px; }\n"
if old_settings not in settings:
    raise SystemExit("settings mobile header marker not found")
settings_path.write_text(settings.replace(old_settings, new_settings, 1), encoding="utf-8")
