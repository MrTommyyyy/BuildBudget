"""Exercise the packaged executable against disposable inputs."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

EXE = Path("dist/BuildBudget.exe").resolve()

def run(*args, code=0):
    result = subprocess.run([str(EXE), *map(str, args)], capture_output=True, text=True, timeout=60)
    if result.returncode != code:
        raise RuntimeError(f"Unexpected exit {result.returncode}: {result.stdout} {result.stderr}")
    return result.stdout

assert run("--version").strip() == "0.2.0"
assert json.loads(run("walls", 3, 3, 3, "--extra-percent", 10, "--json"))["total_blocks"] == 27
assert json.loads(run("circle", 2, "--inner-radius", 1, "--json"))["base_blocks"] == 8
run("walls", -1, 3, 3, code=1)
print("Packaged executable smoke checks passed")
