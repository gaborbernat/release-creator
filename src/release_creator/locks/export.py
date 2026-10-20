"""Preserve uv's resolved selections in a PEP 751 export."""

lazy import json
lazy import shutil
lazy import subprocess  # ruff: ignore[suspicious-subprocess-import]  # uv owns the project resolver.
lazy import tomllib
lazy from collections import defaultdict
lazy from pathlib import Path
lazy from typing import Any

lazy import tomli_w


def export_lock(project: Path, output: Path, tool_python: str | None = None) -> None:
    """Export each resolved group and extra with its selection marker.

    Raises:
        ValueError: The project cannot describe a selectable lock.
        FileNotFoundError: uv is not installed.

    """
    data = tomllib.loads(project.read_text(encoding="utf-8"))
    requires_python, groups, extras, export_scope = _project_selections(project, data, tool_python)
    if "project-runtime" in groups:
        msg = "project-runtime is reserved for the project's runtime dependencies"
        raise ValueError(msg)
    lock_path = project.parent / "uv.lock"
    created_lock = not lock_path.exists()
    if (uv := shutil.which("uv")) is None:
        msg = "uv is required to export a project lock"
        raise FileNotFoundError(msg)
    try:
        _run_uv(uv, project.parent, "lock")
        packages: dict[str, dict[str, object]] = {}
        markers: dict[str, set[str]] = defaultdict(set)
        selections = [("project-runtime", "dependency_groups", ["--no-default-groups"])]
        selections.extend((group, "dependency_groups", ["--only-group", group]) for group in groups)
        selections.extend((extra, "extras", ["--no-default-groups", "--extra", extra]) for extra in extras)
        for name, kind, options in selections:
            exported = _run_uv(uv, project.parent, "export", "--format", "pylock.toml", *export_scope, *options)
            for package in tomllib.loads(exported)["packages"]:
                environment = package.pop("marker", None)
                key = json.dumps(package, sort_keys=True, default=str)
                packages[key] = package
                selection = f"{json.dumps(name)} in {kind}"
                markers[key].add(f"({selection} and ({environment}))" if environment else selection)
        lock = {
            "lock-version": "1.0",
            "created-by": "release-creator (uv)",
            "requires-python": requires_python,
            "extras": extras,
            "dependency-groups": ["project-runtime", *groups],
            "default-groups": [],
            "packages": [],
        }
        for key, package in sorted(
            packages.items(), key=lambda entry: (entry[1]["name"], entry[1].get("version", ""), entry[0])
        ):
            package["marker"] = " or ".join(sorted(markers[key]))
            lock["packages"].append(package)
        output.write_text(tomli_w.dumps(lock), encoding="utf-8")
    finally:
        if created_lock:
            lock_path.unlink(missing_ok=True)


def _project_selections(
    project: Path, data: dict[str, Any], tool_python: str | None
) -> tuple[str, list[str], list[str], list[str]]:
    members = data.get("tool", {}).get("uv", {}).get("workspace", {}).get("members", [])
    projects = [data]
    projects.extend(
        tomllib.loads((project.parent / member / "pyproject.toml").read_text(encoding="utf-8")) for member in members
    )
    ranges = {item["project"]["requires-python"] for item in projects if "requires-python" in item.get("project", {})}
    if len(ranges) > 1:
        msg = "workspace members must share a requires-python range"
        raise ValueError(msg)
    if (requires_python := next(iter(ranges), tool_python)) is None:
        msg = "declare [project].requires-python or pass --tool-python for a tool-only project"
        raise ValueError(msg)
    groups = list(dict.fromkeys(group for item in projects for group in item.get("dependency-groups", {})))
    extras = list(
        dict.fromkeys(extra for item in projects for extra in item.get("project", {}).get("optional-dependencies", {}))
    )
    return (
        requires_python,
        groups,
        extras,
        ["--all-packages", "--no-emit-workspace"] if members else ["--no-emit-project"],
    )


def _run_uv(uv: str, directory: Path, *arguments: str) -> str:
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]  # Fixed uv argv.
        [uv, *arguments], cwd=directory, check=False, capture_output=True, text=True
    )
    if result.returncode:
        msg = result.stderr.strip() or f"uv {arguments[0]} failed"
        raise ValueError(msg)
    return result.stdout


__all__ = [
    "export_lock",
]
