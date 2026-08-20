from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
REQUIRED_FRONTMATTER = {
    "tags",
    "title",
    "summary",
    "related",
    "created_on",
    "updated_on",
    "status",
}
ALLOWED_STATUSES = {
    "active",
    "draft",
    "paused",
    "completed",
    "archived",
    "superseded",
    # A record that reached a conclusion and is not being worked. Distinct from `paused`, which
    # implies resumption, and from `completed`, which implies the question was answered.
    "inactive",
}
HYPOTHESIS_OUTCOMES = {"untested", "rejected", "revised", "advanced", "unresolved"}
EXPERIMENT_OUTCOMES = {"pending", "rejected", "revised", "advanced", "inconclusive"}
RESEARCH_DIRECTORY = re.compile(r"R(?P<number>\d{2})-(?P<title>[a-z0-9]+(?:-[a-z0-9]+)*)$")
HYPOTHESIS_FILE = re.compile(r"(?P<id>H\d{2})-(?P<title>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
EXPERIMENT_FILE = re.compile(r"(?P<id>E\d{2})-(?P<title>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
IDEA_FILE = re.compile(r"(?P<id>I\d{3})-(?P<title>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
SESSION_FILE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<title>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")
MARKDOWN_LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")
RESEARCH_COLLECTIONS = {"docs", "hypothesis", "experiments"}


def _markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
    )


def _frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text().splitlines()
    assert lines and lines[0] == "---", f"{path.relative_to(ROOT)} has no YAML frontmatter"
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"{path.relative_to(ROOT)} has unclosed YAML frontmatter") from error

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if line and not line.startswith((" ", "-")) and ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def _inline_list(value: str) -> list[str]:
    assert value.startswith("[") and value.endswith("]")
    return [item.strip().strip("\"'") for item in value[1:-1].split(",") if item.strip()]


def _headings(path: Path) -> set[str]:
    return {line.strip() for line in path.read_text().splitlines() if line.startswith("## ")}


def test_every_markdown_file_has_graph_frontmatter() -> None:
    for path in _markdown_files():
        values = _frontmatter(path)
        missing = REQUIRED_FRONTMATTER - values.keys()
        assert not missing, f"{path.relative_to(ROOT)} is missing {sorted(missing)}"
        assert values["title"] not in {"", '""'}, f"{path.relative_to(ROOT)} has no title"
        assert values["summary"] not in {"", '""'}, f"{path.relative_to(ROOT)} has no summary"
        tags = _inline_list(values["tags"])
        related = _inline_list(values["related"])
        assert tags and all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", tag) for tag in tags)
        assert related, f"{path.relative_to(ROOT)} must connect to at least one related document"
        for target in related:
            assert (ROOT / target).is_file(), (
                f"{path.relative_to(ROOT)} has missing related document: {target}"
            )
        assert DATE.fullmatch(values["created_on"])
        assert DATE.fullmatch(values["updated_on"])
        assert values["status"] in ALLOWED_STATUSES


def test_docs_notebooks_data_and_source_share_research_titles() -> None:
    docs_root = ROOT / "docs" / "research"
    notebooks_root = ROOT / "notebooks"
    data_root = ROOT / "data"
    docs = {path.name for path in docs_root.iterdir() if path.is_dir()}
    notebooks = {path.name for path in notebooks_root.iterdir() if path.is_dir()}
    data = {path.name for path in data_root.iterdir() if path.is_dir()}

    assert docs == notebooks
    assert docs == data
    assert docs, "at least one numbered research directory is required"

    for directory_name in docs:
        match = RESEARCH_DIRECTORY.fullmatch(directory_name)
        assert match, f"invalid research directory: {directory_name}"
        domain = match.group("title")
        package = ROOT / "src" / "parallax" / domain.replace("-", "_")
        assert package.is_dir(), f"missing domain package: {package.relative_to(ROOT)}"

        domain_data = data_root / directory_name
        assert (domain_data / "raw").is_dir()
        assert (domain_data / "processed").is_dir()

        collections = {
            path.name for path in (docs_root / directory_name).iterdir() if path.is_dir()
        }
        missing_collections = RESEARCH_COLLECTIONS - collections
        assert not missing_collections, (
            f"{directory_name} is missing research collections: {sorted(missing_collections)}"
        )

        for root in (
            docs_root / directory_name,
            notebooks_root / directory_name,
            domain_data,
        ):
            for path in root.rglob("*.md"):
                values = _frontmatter(path)
                assert values.get("research_id") == f"R{match.group('number')}"
                assert values.get("domain") == domain


def test_hypothesis_and_experiment_records_follow_their_contracts() -> None:
    for research_root in sorted((ROOT / "docs" / "research").glob("R??-*")):
        match = RESEARCH_DIRECTORY.fullmatch(research_root.name)
        assert match
        research_id = f"R{match.group('number')}"
        domain = match.group("title")
        hypotheses: dict[str, Path] = {}

        for path in sorted((research_root / "hypothesis").glob("*.md")):
            if path.name == "README.md":
                continue
            file_match = HYPOTHESIS_FILE.fullmatch(path.name)
            assert file_match, f"invalid hypothesis filename: {path.relative_to(ROOT)}"
            values = _frontmatter(path)
            hypothesis_id = file_match.group("id")
            assert values.get("research_id") == research_id
            assert values.get("domain") == domain
            assert values.get("hypothesis_id") == hypothesis_id
            assert values.get("outcome") in HYPOTHESIS_OUTCOMES
            assert hypothesis_id not in hypotheses
            hypotheses[hypothesis_id] = path
            assert {
                "## Claim",
                "## Baseline",
                "## Rejection criteria",
                "## Experiment queue",
                "## Decision history",
            } <= _headings(path)

        experiment_ids: set[str] = set()
        for path in sorted((research_root / "experiments").glob("*.md")):
            if path.name == "README.md":
                continue
            file_match = EXPERIMENT_FILE.fullmatch(path.name)
            assert file_match, f"invalid experiment filename: {path.relative_to(ROOT)}"
            values = _frontmatter(path)
            experiment_id = file_match.group("id")
            assert values.get("research_id") == research_id
            assert values.get("domain") == domain
            assert values.get("experiment_id") == experiment_id
            assert experiment_id not in experiment_ids
            experiment_ids.add(experiment_id)

            hypothesis_id = values.get("hypothesis_id")
            assert hypothesis_id in hypotheses, (
                f"{path.relative_to(ROOT)} references missing local hypothesis {hypothesis_id}"
            )
            hypothesis_path = hypotheses[hypothesis_id].relative_to(ROOT).as_posix()
            assert hypothesis_path in _inline_list(values["related"]), (
                f"{path.relative_to(ROOT)} must link its primary hypothesis in related"
            )
            outcome = values.get("outcome")
            assert outcome in EXPERIMENT_OUTCOMES, (
                f"{path.relative_to(ROOT)} has unknown outcome {outcome!r}"
            )

            # The experiment record type means two different things unless this is explicit:
            # a plan frozen before the data was opened, and a write-up of work already done.
            # Only the first kind can promote a claim.
            preregistered = values.get("preregistered")
            assert preregistered in {"true", "false"}, (
                f"{path.relative_to(ROOT)} must declare preregistered: true or false"
            )
            assert not (preregistered == "false" and outcome == "advanced"), (
                f"{path.relative_to(ROOT)} cannot advance a claim: its method was written after "
                f"the data was seen. Register a new preregistered experiment instead."
            )
            assert {"## Methodology", "## Results", "## Outcome"} <= _headings(path)

            notebook_dir = ROOT / "notebooks" / research_root.name
            methodologies = [
                candidate
                for candidate in notebook_dir.iterdir()
                if candidate.is_file()
                and candidate.suffix in {".ipynb", ".py"}
                and candidate.name.startswith(f"{experiment_id}-")
            ]
            assert methodologies, (
                f"{path.relative_to(ROOT)} has no methodology at "
                f"notebooks/{research_root.name}/{experiment_id}-*.ipynb or .py"
            )
            body = path.read_text()
            assert any(
                methodology.relative_to(ROOT).as_posix() in body or methodology.name in body
                for methodology in methodologies
            ), (
                f"{path.relative_to(ROOT)} must name its "
                f"notebooks/{research_root.name}/{experiment_id}-* methodology"
            )


def test_idea_and_session_records_follow_their_contracts() -> None:
    for path in sorted((ROOT / "docs" / "ideas").glob("*.md")):
        if path.name == "README.md":
            continue
        match = IDEA_FILE.fullmatch(path.name)
        assert match, f"invalid idea filename: {path.relative_to(ROOT)}"
        values = _frontmatter(path)
        assert values.get("idea_id") == match.group("id")
        assert {"## Idea", "## Possible destination", "## Graduation history"} <= _headings(path)

    for path in sorted((ROOT / "docs" / "sessions").glob("*.md")):
        if path.name == "README.md":
            continue
        match = SESSION_FILE.fullmatch(path.name)
        assert match, f"invalid session filename: {path.relative_to(ROOT)}"
        values = _frontmatter(path)
        assert values.get("session_date") == match.group("date")
        assert {
            "## Objective",
            "## Decisions",
            "## Work completed",
            "## Open threads",
            "## Resume here",
        } <= _headings(path)


def test_record_templates_define_required_sections() -> None:
    templates = ROOT / "docs" / "_templates"
    assert {
        "## Claim",
        "## Baseline",
        "## Rejection criteria",
        "## Experiment queue",
        "## Decision history",
    } <= _headings(templates / "HYPOTHESIS.md")
    assert {"## Methodology", "## Results", "## Outcome"} <= _headings(templates / "EXPERIMENT.md")
    assert "preregistered: true" in (templates / "EXPERIMENT.md").read_text(), (
        "the experiment template must carry the preregistration declaration it requires"
    )
    assert {"## Idea", "## Possible destination", "## Graduation history"} <= _headings(
        templates / "IDEA.md"
    )
    assert {
        "## Objective",
        "## Decisions",
        "## Work completed",
        "## Open threads",
        "## Resume here",
    } <= _headings(templates / "SESSION.md")


def test_local_markdown_links_resolve() -> None:
    for path in _markdown_files():
        for raw_target in MARKDOWN_LINK.findall(path.read_text()):
            target = raw_target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (path.parent / target).resolve()
            assert candidate.exists(), (
                f"{path.relative_to(ROOT)} has missing Markdown link: {raw_target}"
            )
