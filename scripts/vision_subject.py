"""One strict, shared authoring contract for the four pillars and four principles.

The Markdown is the source of truth. The public JSON and site disclosures are
projections of it, not independently maintained editorial copies.
"""
from __future__ import annotations

import re

SECTIONS = ("Statement", "Explanation", "Aspirations")
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


def validate_aspiration_details(details: str, label: str) -> None:
    """Lists guide decisions; they cannot substitute for the explanatory prose."""
    markers = list(re.finditer(r"(?m)^\*\*(We should(?: never)?):\*\*[ \t]*$", details))
    prose = details[:markers[0].start()].strip() if markers else details.strip()
    if len(prose.split()) < 15:
        raise ValueError(f"{label}: details are too thin; write at least 15 words of prose before the lists")
    if re.search(r"(?m)^[-*] ", prose):
        raise ValueError(f"{label}: aspiration bullets belong under We should / We should never")
    if not markers:
        if "We should:" in details or "We should never:" in details:
            raise ValueError(f"{label}: use the standalone bold We should / We should never labels")
        return
    if [m.group(1) for m in markers] != ["We should", "We should never"]:
        raise ValueError(f"{label}: We should and We should never must appear together, in that order")
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(details)
        lines = [line for line in details[marker.end():end].strip().splitlines() if line.strip()]
        if not 1 <= len(lines) <= 5 or any(not re.match(r"^[-*] ", line) for line in lines):
            raise ValueError(f"{label}: {marker.group(1)} needs 1-5 single-line bullets and no trailing prose")
        for line in lines:
            one_sentence(line[2:], f"{label}: {marker.group(1)} bullet")


def parse_subject(text: str, path: str) -> dict:
    """Validate and parse either kind of vision subject, without interpreting merit."""
    if not text.startswith("# ") or not text.splitlines()[0][2:].strip():
        raise ValueError(f"{path}: missing subject title")
    headings = list(SECTION.finditer(text))
    names = [m.group(1).strip() for m in headings]
    if names not in [list(SECTIONS), [*SECTIONS, "References"]]:
        raise ValueError(f"{path}: sections must be Statement, Explanation, Aspirations, optional References, in order")
    parts = {}
    for idx, match in enumerate(headings):
        end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
        parts[match.group(1).strip()] = text[match.end():end].strip()

    statement = one_sentence(parts["Statement"], f"{path}: Statement", limit=180)
    explanation = parts["Explanation"]
    if ("\n\n" in explanation or "\n" in explanation or
            not 20 <= len(explanation.split()) <= 105):
        raise ValueError(f"{path}: Explanation needs one short paragraph (20-105 words)")
    body = parts["Aspirations"]
    marks = list(CHARACTERISTIC.finditer(body))
    if not 2 <= len(marks) <= 6 or body[:marks[0].start()].strip():
        raise ValueError(f"{path}: needs 2-6 directly headed aspirations")
    characteristics = []
    for idx, mark in enumerate(marks):
        title = mark.group(1).strip()
        end = marks[idx + 1].start() if idx + 1 < len(marks) else len(body)
        rest = body[mark.end():end].strip()
        summary, sep, details = rest.partition("\n\n")
        if not sep or not details.strip() or "### " in details:
            raise ValueError(f"{path}: {title}: needs a summary sentence then detailed prose")
        summary = one_sentence(summary, f"{path}: {title} summary")
        validate_aspiration_details(details, f"{path}: {title}")
        if not 3 <= len(title) <= 65 or not SLUG.fullmatch(slug(title)):
            raise ValueError(f"{path}: invalid aspiration title: {title!r}")
        characteristics.append({
            "id": slug(title), "title": title,
            "summary": summary, "detailsMarkdown": details.strip(),
        })
    if len({c["id"] for c in characteristics}) != len(characteristics):
        raise ValueError(f"{path}: aspiration IDs must be unique")
    references = parts.get("References", "")
    if "References" in names and not references:
        raise ValueError(f"{path}: empty References section")
    return {
        "statement": statement, "explanationMarkdown": explanation,
        "characteristics": characteristics, "referencesMarkdown": references,
    }


def render_subject_markdown(subject: dict) -> str:
    """Legacy bodyMarkdown remains derived, never separately authored."""
    chunks = [subject["statement"], subject["explanationMarkdown"], "## Aspirations"]
    for characteristic in subject["characteristics"]:
        chunks.append("### " + characteristic["title"])
        chunks.append(characteristic["summary"])
        chunks.append(characteristic["detailsMarkdown"])
    if subject["referencesMarkdown"]:
        chunks.extend(["## References", subject["referencesMarkdown"]])
    return "\n\n".join(chunks)
