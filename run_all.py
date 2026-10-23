"""Run every Python example of Volume 1A and report what works.

Run from the northbridge folder, with .venv active:
    python run_all.py            # every chapter
    python run_all.py 12 13      # only Chapters 12 and 13

Scripts that need SQL Server (pyodbc), the local API or Java are skipped,
with the reason, when that service is not available on your computer.
The book's own files only are run: your my_ files are left alone.
"""
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODE = ROOT / "code"
TIMEOUT = 300
# scripts written to show an error message: a failure is the expected result
EXPECTED_ERROR = {"raise_error.py", "scope.py", "step2_checks.py"}
DEMO_KEY = "northbridge-demo"   # the local API's practice key (Chapter 16)


def api_running():
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2):
            return True
    except OSError:
        return False


def has_module(name):
    r = subprocess.run([sys.executable, "-c", f"import {name}"],
                       capture_output=True)
    return r.returncode == 0


def internet_ok():
    try:
        with urllib.request.urlopen("https://api.frankfurter.dev", timeout=5):
            return True
    except OSError:
        return False


def java_ok():
    try:
        return subprocess.run(["java", "-version"], capture_output=True,
                              timeout=30).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def run(script, env):
    try:
        r = subprocess.run([sys.executable, str(script.relative_to(ROOT))],
                           cwd=ROOT, capture_output=True, text=True,
                           timeout=TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    ok = (r.returncode == 0) != (script.name in EXPECTED_ERROR)
    last = (r.stderr.strip().splitlines() or [""])[-1]
    return ok, last


def main():
    wanted = {f"{int(a):02d}" for a in sys.argv[1:]}
    (ROOT / "output").mkdir(exist_ok=True)
    api, spark = api_running(), has_module("pyspark") and java_ok()
    web = internet_ok()
    env = dict(os.environ)
    env.setdefault("NB_API_KEY", DEMO_KEY)
    ok_count, skipped, failed = 0, 0, []
    for folder in sorted(CODE.iterdir()):
        n = folder.name[:2]
        if not folder.is_dir() or n == "00" or (wanted and n not in wanted):
            continue
        for script in sorted(folder.rglob("*.py")):
            if script.name.startswith(("my_", "_")):
                continue
            text = script.read_text(encoding="utf-8", errors="ignore")
            why = None
            if any(k in text for k in ("pyodbc", "mssql", "nb_db", "create_engine")):
                why = "needs SQL Server (run it yourself, Chapter 15)"
            elif "127.0.0.1:8000" in text and not api:
                why = "needs the local API (Chapter 8)"
            elif "frankfurter" in text and not web:
                why = "needs internet access"
            elif "pyspark" in text and not spark:
                why = "needs Java and PySpark (Chapter 22)"
            elif "input(" in text:
                why = "asks for keyboard input"
            if why:
                skipped += 1
                print(f"SKIPPED  {script.relative_to(ROOT)}  ({why})")
                continue
            ok, last = run(script, env)
            if ok:
                ok_count += 1
            else:
                failed.append(script)
    # a script may read a file that a later script in the same folder writes
    # (alphabetical order is not the book's order): retry the failures once
    still = []
    for script in failed:
        ok, last = run(script, env)
        if ok:
            ok_count += 1
        else:
            still.append(script)
            print(f"FAILED   {script.relative_to(ROOT)}  {last}")
    print(f"\n{ok_count} OK, {len(still)} failed, {skipped} skipped")


if __name__ == "__main__":
    main()
