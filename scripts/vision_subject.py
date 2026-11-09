"""One strict, shared authoring contract for the four pillars and four principles.

The Markdown is the source of truth. The public JSON and site disclosures are
projections of it, not independently maintained editorial copies.
"""
from __future__ import annotations

import re

SECTIONS = ("Statement", "Explanation", "Characteristics")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECTION = re.compile(r"^## ([^\n]+)[ \t]*$", re.M)
CHARACTERISTIC = re.compile(r"^### ([^\n]+)[ \t]*$", re.M)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower().replace("'", "")).strip("-")


def one_sentence(value: str, label: str, *, limit: int = 210) -> str:
    value = value.strip()
    if ("\n" in value or len(value) < 20 or len(value) > limit or
            not value.endswith((".", "!", "?")) or
            len(re.split(r"(?<=[.!?])\s+", value)) != 1 or
            re.search(r"^[-*] ", value)):
        raise ValueError(f"{label}: needs one complete, concise sentence")
    return value


def parse_subject(text: str, path: str) -> dict:
    """Validate and parse either kind of vision subject, without interpreting merit."""
    if not text.startswith("# ") or not text.splitlines()[0][2:].strip():
        raise ValueError(f"{path}: missing subject title")
    headings = list(SECTION.finditer(text))
    names = [m.group(1).strip() for m in headings]
    if names not in [list(SECTIONS), [*SECTIONS, "References"]]:
        raise ValueError(f"{path}: sections must be Statement, Explanation, Characteristics, optional References, in order")
    parts = {}
    for idx, match in enumerate(headings):
        end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
        parts[match.group(1).strip()] = text[match.end():end].strip()

    statement = one_sentence(parts["Statement"], f"{path}: Statement", limit=180)
    explanation = parts["Explanation"]
    if ("\n\n" in explanation or "\n" in explanation or
            not 20 <= len(explanation.split()) <= 105):
        raise ValueError(f"{path}: Explanation needs one short paragraph (20-105 words)")
    body = parts["Characteristics"]
    marks = list(CHARACTERISTIC.finditer(body))
    if not 2 <= len(marks) <= 6 or body[:marks[0].start()].strip():
        raise ValueError(f"{path}: needs 2-6 directly headed characteristics")
    characteristics = []
    for idx, mark in enumerate(marks):
        title = mark.group(1).strip()
        end = marks[idx + 1].start() if idx + 1 < len(marks) else len(body)
        rest = body[mark.end():end].strip()
        summary, sep, details = rest.partition("\n\n")
        if not sep or not details.strip() or "### " in details:
            raise ValueError(f"{path}: {title}: needs a summary sentence then detailed prose")
        summary = one_sentence(summary, f"{path}: {title} summary")
        if len(details.split()) < 15:
            raise ValueError(f"{path}: {title}: details are too thin")
        if not 3 <= len(title) <= 65 or not SLUG.fullmatch(slug(title)):
            raise ValueError(f"{path}: invalid characteristic title: {title!r}")
        characteristics.append({
            "id": slug(title), "title": title,
            "summary": summary, "detailsMarkdown": details.strip(),
        })
    if len({c["id"] for c in characteristics}) != len(characteristics):
        raise ValueError(f"{path}: characteristic IDs must be unique")
    references = parts.get("References", "")
    if "References" in names and not references:
        raise ValueError(f"{path}: empty References section")
    return {
        "statement": statement, "explanationMarkdown": explanation,
        "characteristics": characteristics, "referencesMarkdown": references,
    }


def render_subject_markdown(subject: dict) -> str:
    """Legacy bodyMarkdown remains derived, never separately authored."""
    chunks = [subject["statement"], subject["explanationMarkdown"], "## Characteristics"]
    for characteristic in subject["characteristics"]:
        chunks.append("### " + characteristic["title"])
        chunks.append(characteristic["summary"])
        chunks.append(characteristic["detailsMarkdown"])
    if subject["referencesMarkdown"]:
        chunks.extend(["## References", subject["referencesMarkdown"]])
    return "\n\n".join(chunks)
