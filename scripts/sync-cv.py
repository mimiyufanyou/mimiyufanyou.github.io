"""Copy the CV from the job-search repo's blocks into src/data/cv.json.

The job-search repo (local only) holds the CV as blocks: resume/blocks/*.toml.
This page shows the same words. Run this after changing them:

    python3 scripts/sync-cv.py

What it leaves out, on purpose:
- contact details (the renderer reads those from the Keychain; they never live here)
- parked roles (`parked = true`) and bullets she hasn't approved (`confirm = true`)
- certificates tagged "personal"
"""

import json
import tomllib
from pathlib import Path

BLOCKS = Path.home() / "Desktop/github.nosync/job-search/resume/blocks"
OUT = Path(__file__).resolve().parent.parent / "src" / "data" / "cv.json"

HEADLINE = "data-science"  # which [[headline]] in profile.toml leads the page

CV_MONTHS = "Jan Feb March Apr May June Jul Aug Sep Oct Nov Dec".split()


def cvdate(s: str) -> str:
    """Her CV's date style: "Dec ’23", "June ’26"."""
    if s == "present":
        return "Present"
    y, m = s.split("-")
    return f"{CV_MONTHS[int(m) - 1]} ’{y[2:]}"


def main() -> None:
    exp = tomllib.loads((BLOCKS / "experience.toml").read_text())
    prof = tomllib.loads((BLOCKS / "profile.toml").read_text())

    roles = []
    for r in exp["role"]:
        if r.get("parked"):
            continue
        groups: dict[str, list[str]] = {}
        for b in r.get("bullet", []):
            if b.get("confirm"):
                continue
            groups.setdefault(b.get("section", r["label"]), []).append(b["text"].rstrip("."))
        roles.append({
            "employer": r["employer"],
            "team": r.get("team", ""),
            "title": r["title"],
            "location": r["location"],
            "dates": f"{cvdate(r['start'])} – {cvdate(r['end'])}",
            "tools": r.get("tools", []),
            "groups": [{"label": k, "bullets": v} for k, v in groups.items()],
        })

    head = next(h for h in prof["headline"] if h["id"] == HEADLINE)
    cv = {
        "headline": {"title": head["title"], "summary": head["summary"]},
        "roles": roles,
        "education": [
            {"school": e["school"], "degree": e["degree"],
             "dates": f"{cvdate(e['start'])} – {cvdate(e['end'])}", "notes": e.get("notes", [])}
            for e in prof.get("education", [])
        ],
        "certificates": [
            {"name": c["name"], "dates": f"{cvdate(c['start'])} – {cvdate(c['end'])}"}
            for c in prof.get("certificate", []) if "personal" not in c.get("tags", [])
        ],
        "projects": [{"name": p["name"], "text": p["text"]} for p in prof.get("project", [])],
        "interests": prof.get("interests", []),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cv, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}: {len(roles)} roles, {sum(len(g['bullets']) for r in roles for g in r['groups'])} bullets")


if __name__ == "__main__":
    main()
