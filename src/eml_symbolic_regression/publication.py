"""Publication-grade rebuild and provenance helpers."""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


DEFAULT_V113_PUBLICATION_DIR = Path("artifacts") / "paper" / "v1.13"
DEFAULT_LOCKFILE = Path("requirements-lock.txt")
DEFAULT_CONTAINER_FILE = Path("Dockerfile")
FORBIDDEN_PLACEHOLDER_TOKENS = (
    "1970-01-01T00:00:00+00:00",
    '"snapshot"',
)


class PublicationRebuildError(RuntimeError):
    """Raised when publication package generation fails."""


@dataclass(frozen=True)
class PublicationRebuildPaths:
    output_dir: Path
    manifest_json: Path
    source_locks_json: Path
    reproduction_md: Path
    validation_json: Path
    validation_md: Path

    def as_dict(self) -> dict[str, str]:
        return {key: str(value) for key, value in self.__dict__.items()}


def write_publication_rebuild(
    *,
    output_dir: Path = DEFAULT_V113_PUBLICATION_DIR,
    smoke: bool = False,
    overwrite: bool = False,
    allow_dirty: bool = True,
    command: str | None = None,
    allowed_placeholder_paths: Iterable[str] = (),
) -> PublicationRebuildPaths:
    """Write a v1.13 publication rebuild package with source and output provenance."""

    output_dir = Path(output_dir)
    paths = PublicationRebuildPaths(
        output_dir=output_dir,
        manifest_json=output_dir / "manifest.json",
        source_locks_json=output_dir / "source-locks.json",
        reproduction_md=output_dir / "reproduction.md",
        validation_json=output_dir / "validation.json",
        validation_md=output_dir / "validation.md",
    )
    if output_dir.exists() and overwrite:
        _remove_existing_output_dir(output_dir)
    if paths.manifest_json.exists() and not overwrite:
        raise PublicationRebuildError(f"{paths.manifest_json} already exists; pass overwrite=True to refresh")
    output_dir.mkdir(parents=True, exist_ok=True)

    git = _git_metadata()
    if git["dirty"] and not allow_dirty:
        raise PublicationRebuildError("publication rebuild requires a clean git tree unless allow_dirty=True")

    run_command = command or _default_rebuild_command(output_dir=output_dir, smoke=smoke)
    inputs = _default_source_inputs()
    source_lock_payload = {
        "schema": "eml.v113_publication_source_locks.v1",
        "generated_at": _now_iso(),
        "inputs": inputs,
        "input_count": len(inputs),
    }
    _write_json(paths.source_locks_json, source_lock_payload)
    paths.reproduction_md.write_text(
        _reproduction_markdown(output_dir=output_dir, command=run_command, smoke=smoke),
        encoding="utf-8",
    )
    paths.validation_md.write_text(
        "# Publication Validation\n\nValidation details are written to `validation.json`.\n",
        encoding="utf-8",
    )

    manifest = {
        "schema": "eml.v113_publication_rebuild.v1",
        "generated_at": _now_iso(),
        "mode": "smoke" if smoke else "full",
        "output_dir": str(output_dir),
        "command": run_command,
        "git": git,
        "environment": _environment_metadata(),
        "inputs": inputs,
        "outputs": _output_locks((paths.source_locks_json, paths.reproduction_md, paths.validation_md)),
        "claim_boundary": (
            "Phase 69 validates rebuild/provenance mechanics; full v1.13 evidence generation "
            "and public release are handled by later publication gates."
        ),
    }
    _write_json(paths.manifest_json, manifest)

    validation = validate_publication_package(output_dir, allowed_placeholder_paths=allowed_placeholder_paths)
    _write_json(paths.validation_json, validation)
    paths.validation_md.write_text(_validation_markdown(validation), encoding="utf-8")
    manifest["outputs"] = _output_locks((paths.source_locks_json, paths.reproduction_md, paths.validation_json, paths.validation_md))
    manifest["validation"] = {
        "status": validation["status"],
        "validation_json": str(paths.validation_json),
        "validation_markdown": str(paths.validation_md),
    }
    _write_json(paths.manifest_json, manifest)
    return paths


def validate_publication_package(
    output_dir: Path,
    *,
    allowed_placeholder_paths: Iterable[str] = (),
) -> dict[str, Any]:
    """Validate provenance hashes and placeholder metadata policy for a publication package."""

    output_dir = Path(output_dir)
    manifest_path = output_dir / "manifest.json"
    checks: list[dict[str, Any]] = []
    if not manifest_path.is_file():
        _check(checks, "manifest_present", False, "manifest.json exists", {"path": str(manifest_path)})
        return _validation_payload(checks)

    manifest = _read_json(manifest_path)
    required_fields = ("schema", "generated_at", "mode", "command", "git", "environment", "inputs", "outputs")
    _check(
        checks,
        "manifest_required_fields",
        all(field in manifest for field in required_fields),
        "Manifest has required publication provenance fields.",
        {"missing": [field for field in required_fields if field not in manifest]},
    )
    _check(
        checks,
        "manifest_schema",
        manifest.get("schema") == "eml.v113_publication_rebuild.v1",
        "Manifest uses the v1.13 publication rebuild schema.",
        {"schema": manifest.get("schema")},
    )
    _validate_hash_rows(checks, manifest.get("inputs", []), row_kind="input")
    _validate_hash_rows(checks, manifest.get("outputs", []), row_kind="output")
    _validate_placeholders(checks, output_dir, allowed_placeholder_paths)
    return _validation_payload(checks)


def _default_source_inputs() -> list[dict[str, Any]]:
    paths = (
        Path("pyproject.toml"),
        Path("requirements-lock.txt"),
        Path("Dockerfile"),
        Path("src/eml_symbolic_regression/cli.py"),
        Path("src/eml_symbolic_regression/publication.py"),
        Path("sources/NORTH_STAR.md"),
        Path("sources/FOR_DEMO.md"),
    )
    rows = []
    for path in paths:
        if path.is_file():
            rows.append(_lock_row("source_input", path))
    return rows


def _remove_existing_output_dir(output_dir: Path) -> None:
    resolved = output_dir.resolve()
    forbidden = {Path.cwd().resolve(), Path("/").resolve()}
    if Path.home().exists():
        forbidden.add(Path.home().resolve())
    if resolved in forbidden:
        raise PublicationRebuildError(f"refusing to overwrite unsafe output directory: {output_dir}")
    shutil.rmtree(output_dir)


def _output_locks(paths: Iterable[Path]) -> list[dict[str, Any]]:
    return [_lock_row("generated_output", path) for path in paths if path.is_file()]


def _lock_row(role: str, path: Path) -> dict[str, Any]:
    return {
        "role": role,
        "path": str(path),
        "sha256": _sha256(path),
        "bytes": path.stat().st_size,
    }


def _validate_hash_rows(checks: list[dict[str, Any]], rows: Any, *, row_kind: str) -> None:
    if not isinstance(rows, list) or not rows:
        _check(checks, f"{row_kind}_rows_present", False, f"{row_kind} rows are present.", {"rows": rows})
        return
    missing_hash: list[str] = []
    missing_file: list[str] = []
    mismatched: list[str] = []
    for row in rows:
        if not isinstance(row, Mapping):
            missing_hash.append(str(row))
            continue
        path = Path(str(row.get("path") or ""))
        if not path.is_file():
            missing_file.append(str(path))
            continue
        expected = str(row.get("sha256") or "")
        if not expected:
            missing_hash.append(str(path))
        elif _sha256(path) != expected:
            mismatched.append(str(path))
    _check(
        checks,
        f"{row_kind}_hashes_valid",
        not missing_hash and not missing_file and not mismatched,
        f"{row_kind} rows have existing files and valid SHA-256 hashes.",
        {"missing_hash": missing_hash, "missing_file": missing_file, "mismatched": mismatched},
    )


def _validate_placeholders(checks: list[dict[str, Any]], output_dir: Path, allowed_placeholder_paths: Iterable[str]) -> None:
    allowed = {Path(path).as_posix() for path in allowed_placeholder_paths}
    violations: list[dict[str, str]] = []
    for path in sorted(item for item in output_dir.rglob("*") if item.is_file()):
        relative = path.relative_to(output_dir).as_posix()
        if relative in allowed:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN_PLACEHOLDER_TOKENS:
            if token in text:
                violations.append({"path": relative, "token": token})
    _check(
        checks,
        "placeholder_metadata_rejected",
        not violations,
        "No forbidden placeholder metadata appears outside explicit deterministic fixtures.",
        {"violations": violations},
    )


def _validation_payload(checks: list[dict[str, Any]]) -> dict[str, Any]:
    status = "passed" if all(check["status"] == "passed" for check in checks) else "failed"
    return {
        "schema": "eml.v113_publication_validation.v1",
        "generated_at": _now_iso(),
        "status": status,
        "checks": checks,
    }


def _check(checks: list[dict[str, Any]], check_id: str, passed: bool, message: str, details: Mapping[str, Any]) -> None:
    checks.append(
        {
            "id": check_id,
            "status": "passed" if passed else "failed",
            "message": message,
            "details": dict(details),
        }
    )


def _environment_metadata() -> dict[str, Any]:
    lockfile = _optional_file_identity(DEFAULT_LOCKFILE)
    container = _optional_file_identity(DEFAULT_CONTAINER_FILE)
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "lockfile": lockfile,
        "container": container,
    }


def _optional_file_identity(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"path": str(path), "present": False, "sha256": None}
    return {"path": str(path), "present": True, "sha256": _sha256(path)}


def _git_metadata() -> dict[str, Any]:
    revision = _run_git("rev-parse", "HEAD")
    branch = _run_git("rev-parse", "--abbrev-ref", "HEAD")
    status = _run_git("status", "--short")
    return {
        "revision": revision or "unknown",
        "branch": branch or "unknown",
        "dirty": bool(status),
        "status_short": status.splitlines() if status else [],
    }


def _run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ("git", *args),
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _default_rebuild_command(*, output_dir: Path, smoke: bool) -> str:
    parts = [
        "PYTHONPATH=src",
        "python",
        "-m",
        "eml_symbolic_regression.cli",
        "publication-rebuild",
        "--output-dir",
        str(output_dir),
    ]
    if smoke:
        parts.append("--smoke")
    parts.append("--overwrite")
    return " ".join(parts)


def _reproduction_markdown(*, output_dir: Path, command: str, smoke: bool) -> str:
    mode = "smoke" if smoke else "full"
    return "\n".join(
        [
            "# v1.13 Publication Rebuild",
            "",
            f"Mode: `{mode}`",
            "",
            "Run:",
            "",
            "```bash",
            command,
            "```",
            "",
            "The smoke rebuild is a fast provenance and package-shape check. The full publication evidence campaign is a later release gate.",
            f"Output root: `{output_dir}`",
            "",
        ]
    )


def _validation_markdown(validation: Mapping[str, Any]) -> str:
    lines = [
        "# Publication Validation",
        "",
        f"Status: `{validation['status']}`",
        "",
        "| Check | Status |",
        "|-------|--------|",
    ]
    for check in validation.get("checks", []):
        lines.append(f"| {check['id']} | {check['status']} |")
    lines.append("")
    return "\n".join(lines)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
