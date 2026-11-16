"""Reproduce the pre-fix observer's unintended Git clean-filter execution."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

baseline = Path(__file__).with_name("repository_observer_before_filter_fix.py")
spec = importlib.util.spec_from_file_location("observer_before_filter_fix", baseline)
observer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(observer)

with tempfile.TemporaryDirectory(prefix="observer-filter-probe-") as temporary:
    root = Path(temporary)
    repo = root / "repository"
    repo.mkdir()

    def git(*arguments):
        return subprocess.run(["git", "-C", str(repo), *arguments], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    git("init", "--initial-branch=main")
    git("config", "user.name", "Local filter regression probe")
    git("config", "user.email", "local-probe@example.invalid")
    initial = b"Pinned source, revision one.\n"
    (repo / "source.txt").write_bytes(initial)
    git("add", "--", "source.txt")
    git("commit", "-m", "Initial source")
    marker = root / "filter-executed.txt"
    script = root / "recording_filter.py"
    script.write_text(
        "from pathlib import Path\nimport sys\n"
        "Path(" + repr(str(marker)) + ").write_text('filter executed')\n"
        "sys.stdout.buffer.write(sys.stdin.buffer.read())\n", encoding="utf-8")
    (repo / ".gitattributes").write_text("source.txt filter=recording\n", encoding="utf-8")
    git("config", "filter.recording.clean", shlex.quote(sys.executable) + " " + shlex.quote(str(script)))
    git("add", "--", ".gitattributes")
    git("commit", "-m", "Configure local content conversion filter")
    marker.unlink(missing_ok=True)
    (repo / "source.txt").write_bytes(b"x" * len(initial))
    marker_before = marker.exists()
    receipt = observer.capture(repo, ["source.txt"], "offline-filter-regression")
    marker_after = marker.exists()
    result = {
        "kind": "actual-pre-fix-local-git-reproduction",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "baseline": baseline.name,
        "baseline_sha256": hashlib.sha256(baseline.read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "git": git("--version").decode().strip(),
        "changed_file_bytes": len(initial),
        "change_kept_original_length": True,
        "marker_existed_before_capture": marker_before,
        "marker_exists_after_capture": marker_after,
        "marker_contents": marker.read_text() if marker_after else None,
        "capture_status": receipt["status"],
        "captured_git_commands": [x["argv"] for x in receipt["commands"]],
        "finding_reproduced": not marker_before and marker_after,
        "limits": ["same-controller internal review", "local harmless marker only", "no external effects or network"],
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    if not result["finding_reproduced"]:
        raise SystemExit("pre-fix finding was not reproduced")
