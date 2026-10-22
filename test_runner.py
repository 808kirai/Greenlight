import subprocess
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


if __name__ == "__main__":
    path = clone_repo("https://github.com/808kirai/AmaniHaven.git", "main")
    print("Cloned to:", path)
