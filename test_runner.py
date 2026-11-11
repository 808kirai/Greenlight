import os
import subprocess
import sys
import tempfile


def clone_repo(repo_url, branch):
    folder = tempfile.mkdtemp()  # make a temp folder

    result = subprocess.run(
        ["git", "clone", "--branch", branch, "--depth", "1", repo_url, folder],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return folder


def venv_python(venv):
    # windows keeps the venv's python in Scripts, linux and mac keep it in bin
    if os.name == "nt":
        return os.path.join(venv, "Scripts", "python.exe")
    return os.path.join(venv, "bin", "python")


def install_deps(folder):
    venv = os.path.join(folder, ".venv")

    # make a venv inside the cloned repo
    subprocess.run([sys.executable, "-m", "venv", venv], check=True)

    python = venv_python(venv)

    # install the repo's requirements + pytest
    result = subprocess.run(
        [python, "-m", "pip", "install", "-r", os.path.join(folder, "requirements.txt"), "pytest"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return python


if __name__ == "__main__":
    path = clone_repo("https://github.com/808kirai/AmaniHaven.git", "main")
    print("Cloned to:", path)

    python = install_deps(path)
    print("Deps installed:", python)
