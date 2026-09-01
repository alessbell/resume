#!/usr/bin/env python3
"""Generate the website's resume.json + resume.vcf from resume.tex.

resume.tex is the single source of truth; the site's downloadable resume.json
and resume.vcf are derived from it so they can't silently drift. Emits the
site's bespoke JSON shape (contact / skills / experience.roles.accomplishments /
projects), not the JSON-Resume standard. Parses the custom macros:

    \\employerTitle{url}{company}{start - end}
    \\jobLineItem{position}{start - end}      (empty dates inherit the employer's)
    \\resumeItem{title}{description}           -> an accomplishment {title, description}
    \\resumeSubItem{category}{csv}             (Skills section)
    \\resumeSubItem{\\href{url}{name}}{desc (year)}  (Projects section)

plus the heading block for contact fields.

Usage:
    python3 scripts/tex2resume.py resume.tex \\
        --json out/resume.json --vcf out/resume.vcf [--yaml out/resume.yml]

--yaml additionally emits the rendered page's data (_data/resume.yml), in the
JSON-Resume shape Jekyll consumes, so the page is LaTeX-derived too.
"""
import argparse
import json
import re
import sys


def read_group(s, i):
    """s[i] must be '{'. Return (inner_text, index_after_closing_brace)."""
    if s[i] != "{":
        raise ValueError("expected '{' at %d" % i)
    depth, start = 0, i
    while i < len(s):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1 : i], i + 1
        i += 1
    raise ValueError("unbalanced braces from %d" % start)


def read_args(s, i, n):
    """Skip whitespace, then read n brace groups. Return (list, new_index)."""
    args = []
    for _ in range(n):
        while i < len(s) and s[i] in " \t\r\n":
            i += 1
        inner, i = read_group(s, i)
        args.append(inner)
    return args, i


def clean(t):
    """LaTeX fragment -> plain text."""
    t = re.sub(r"\\href\{[^{}]*\}\{([^{}]*)\}", r"\1", t)  # \href{url}{text} -> text
    t = re.sub(r"\\text(?:bf|it|tt|sc)\{([^{}]*)\}", r"\1", t)  # \textbf{x} -> x
    t = t.replace("---", "—").replace("--", "–")  # dashes
    t = t.replace("``", '"').replace("''", '"')  # TeX quotes
    for a, b in ((r"\&", "&"), (r"\%", "%"), (r"\#", "#"), (r"\_", "_"), (r"\$", "$")):
        t = t.replace(a, b)
    t = t.replace("~", " ")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):  # smart -> straight
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def split_dates(d):
    d = d.strip()
    if not d:
        return None, None
    parts = re.split(r"\s+-\s+", d)
    return (parts[0].strip(), parts[1].strip()) if len(parts) == 2 else (d, None)


def parse_contact(heading):
    name = clean(re.search(r"\\LARGE\s+(.+?)\}\}", heading).group(1))
    email = re.search(r"mailto:([^}\s]+)", heading).group(1)

    def href(pat):
        m = re.search(r"\\href\{(https?://[^}]*" + pat + r"[^}]*)\}", heading)
        return m.group(1) if m else None

    lm = re.search(r"\n\s*([A-Za-z][^&\n]*?)\s*&\s*([^\\\n]+?)\s*\\\\", heading)
    return {
        "name": name,
        "email": email,
        "linkedin": href("linkedin"),
        "github": href(r"github\.com"),
        "website": href(r"kyleobrien\.me"),
        "title": clean(lm.group(1)),
        "location": clean(lm.group(2)),
    }


def parse_experience(s):
    exp, emp, role = [], None, None
    macro = re.compile(r"\\(employerTitle|jobLineItem|resumeItem)\b")
    i = 0
    while True:
        m = macro.search(s, i)
        if not m:
            break
        kind = m.group(1)
        if kind == "employerTitle":
            (url, company, dates), i = read_args(s, m.end(), 3)
            st, en = split_dates(dates)
            emp = {"company": clean(company), "companyUrl": url.strip(),
                   "startDate": st, "endDate": en, "roles": []}
            exp.append(emp)
            role = None
        elif kind == "jobLineItem":
            (position, dates), i = read_args(s, m.end(), 2)
            st, en = split_dates(dates)
            if st is None:
                st, en = emp["startDate"], emp["endDate"]
            role = {"title": clean(position), "startDate": st, "endDate": en, "accomplishments": []}
            emp["roles"].append(role)
        else:  # resumeItem
            (title, desc), i = read_args(s, m.end(), 2)
            role["accomplishments"].append({"title": clean(title), "description": clean(desc)})
    return exp


def parse_skills(s):
    out, i = [], 0
    r = re.compile(r"\\resumeSubItem\b")
    while True:
        m = r.search(s, i)
        if not m:
            break
        (category, csv), i = read_args(s, m.end(), 2)
        out.append({"category": clean(category), "items": [clean(k) for k in csv.split(",")]})
    return out


def parse_projects(s):
    out, i = [], 0
    r = re.compile(r"\\resumeSubItem\b")
    while True:
        m = r.search(s, i)
        if not m:
            break
        (titlearg, desc), i = read_args(s, m.end(), 2)
        hm = re.search(r"\\href\{([^{}]*)\}\{([^{}]*)\}", titlearg)
        url, name = (hm.group(1), hm.group(2)) if hm else (None, titlearg)
        desc = clean(desc)
        year = None
        dm = re.search(r"\s*\((\d{4})\)\s*$", desc)
        if dm:
            year, desc = dm.group(1), desc[: dm.start()].strip()
        out.append({"url": url, "title": clean(name), "description": desc, "year": year})
    return out


def yq(s):
    """Double-quoted YAML scalar, matching the hand-authored _data/resume.yml style."""
    if s is None:
        return '""'
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def to_yaml(contact, skills, experience, projects):
    """Emit the page's JSON-Resume-shaped _data/resume.yml from the parsed data."""
    L = ["basics:",
         f"  name: {yq(contact['name'])}",
         f"  label: {yq(contact['title'])}",
         f"  email: {yq(contact['email'])}",
         "  location:",
         f"    region: {yq(contact['location'])}",
         "  profiles:",
         '    - network: "LinkedIn"',
         f"      url: {yq(contact['linkedin'])}",
         '    - network: "GitHub"',
         f"      url: {yq(contact['github'])}",
         "work:"]
    for emp in experience:
        L += [f"  - company: {yq(emp['company'])}",
              f"    website: {yq(emp['companyUrl'])}",
              f"    startDate: {yq(emp['startDate'])}",
              f"    endDate: {yq(emp['endDate'])}",
              "    positions:"]
        for role in emp["roles"]:
            L += [f"      - position: {yq(role['title'])}",
                  f"        startDate: {yq(role['startDate'])}",
                  f"        endDate: {yq(role['endDate'])}",
                  "        highlights:"]
            for acc in role["accomplishments"]:
                L.append(f"          - {yq(acc['title'] + ': ' + acc['description'])}")
    L.append("skills:")
    for sk in skills:
        L += [f"  - name: {yq(sk['category'])}", "    keywords:"]
        L += [f"      - {yq(it)}" for it in sk["items"]]
    L.append("projects:")
    for p in projects:
        L += [f"  - name: {yq(p['title'])}",
              f"    url: {yq(p['url'])}",
              f"    description: {yq(p['description'])}",
              f"    date: {yq(p['year'])}"]
    return "\n".join(L) + "\n"


def build_vcard(c):
    lines = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{c['name']}", f"TITLE:{c['title']}",
             f"EMAIL:{c['email']}"]
    if c.get("linkedin"):
        lines.append(f"URL:{c['linkedin']}")
    if c.get("github"):
        lines.append(f"NOTE:GitHub: {c['github']}")
    if c.get("website"):
        lines.append(f"URL:{c['website']}")
    lines += [f"ADR:;;{c['location']}", "END:VCARD"]
    return "\r\n".join(lines)  # vCard (RFC 6350) mandates CRLF


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--json", required=True)
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--yaml", help="also emit _data/resume.yml (the rendered page's data)")
    args = ap.parse_args()

    tex = open(args.tex, encoding="utf-8").read()
    i_skills = tex.index(r"\section{Skills}")
    i_exp = tex.index(r"\section{Experience}")
    i_proj = tex.index(r"\section{Projects}")
    i_end = tex.index(r"\end{document}")
    heading = tex[tex.index(r"\begin{document}") : i_skills]

    contact = parse_contact(heading)
    resume = {
        "contact": contact,
        "skills": parse_skills(tex[i_skills:i_exp]),
        "experience": parse_experience(tex[i_exp:i_proj]),
        "projects": parse_projects(tex[i_proj:i_end]),
    }
    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(resume, f, indent=2, ensure_ascii=False)  # no trailing newline (matches site files)
    with open(args.vcf, "w", encoding="utf-8", newline="") as f:
        f.write(build_vcard(contact))
    if args.yaml:
        with open(args.yaml, "w", encoding="utf-8") as f:
            f.write(to_yaml(contact, resume["skills"], resume["experience"], resume["projects"]))
    print(f"wrote {args.json} ({len(resume['experience'])} employers), {args.vcf}"
          + (f", {args.yaml}" if args.yaml else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
