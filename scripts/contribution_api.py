"""Small REST transport shared by trusted GitHub contribution workflows."""
from __future__ import annotations
import base64
import json
import os
import urllib.parse
import urllib.request

CATALOG = "plans/index.md"


def plan_text(repository: str, ref: str, folder: str) -> str | None:
    """Read a plain project plan at ref, returning None only for a 404."""
    raise NotImplementedError("PM-7b: project plan reader")


def request(method: str, path: str, payload=None):
    api_root = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        api_root + path, data=data, method=method,
        headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "astrid-dev-contributions",
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read())


def catalog(repository: str, ref: str) -> str:
    owner, name = repository.split("/", 1)
    query = urllib.parse.quote(ref, safe="")
    result = request("GET", f"/repos/{owner}/{name}/contents/{CATALOG}?ref={query}")
    if result.get("type") != "file" or result.get("encoding") != "base64":
        raise ValueError("expected a plain catalog file")
    return base64.b64decode(result["content"]).decode("utf-8")


def changed_files(repo: str, number: int) -> list[dict]:
    files = []
    for page in range(1, 4):
        page_files = request("GET", f"/repos/{repo}/pulls/{number}/files?per_page=100&page={page}")
        files.extend(page_files)
        if len(page_files) < 100:
            return files
    raise ValueError("too many modified files to classify")


def ensure_review_label(repo: str, label: str) -> None:
    """Create one neutral review-queue label if missing. Never grant approval."""
    import urllib.error
    path = f"/repos/{repo}/labels/{urllib.parse.quote(label, safe='')}"
    try:
        request("GET", path)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        try:
            request("POST", f"/repos/{repo}/labels", {
                "name": label,
                "color": "d4c5f9",
                "description": "Submission in review queue; not approved or merged",
            })
        except urllib.error.HTTPError as conflict:
            if conflict.code != 422:
                raise
            request("GET", path)
