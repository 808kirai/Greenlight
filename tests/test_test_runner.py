import os
import subprocess
import sys

import pytest

import test_runner as runner


@pytest.fixture
def local_repo(tmp_path):
    # a tiny git repo on disk so cloning needs no network
    repo = tmp_path / "repo"
    repo.mkdir()
    git = ["git", "-C", str(repo), "-c", "user.name=test", "-c", "user.email=test@example.com"]
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    (repo / "test_sample.py").write_text("def test_ok():\n    assert 1 + 1 == 2\n")
    subprocess.run(git + ["add", "."], check=True)
    subprocess.run(git + ["commit", "-q", "-m", "first"], check=True)
    return str(repo)


def test_venv_python_matches_the_platform():
    path = runner.venv_python("venv")
    expected = os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python")
    assert path == expected


def test_install_args(tmp_path):
    assert runner.install_args(str(tmp_path)) == []
    (tmp_path / "pyproject.toml").write_text("")
    assert runner.install_args(str(tmp_path)) == [str(tmp_path)]
    (tmp_path / "requirements.txt").write_text("")
    assert runner.install_args(str(tmp_path))[0] == "-r"


def test_clone_and_cleanup(local_repo):
    folder = runner.clone_repo(local_repo, "main")
    assert os.path.exists(os.path.join(folder, "test_sample.py"))
    runner.cleanup(folder)
    assert not os.path.exists(folder)


def test_failed_clone_raises_and_leaves_nothing(local_repo, tmp_path, monkeypatch):
    # send the temp folder somewhere we can look inside
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr(runner.tempfile, "tempdir", str(scratch))
    with pytest.raises(RuntimeError):
        runner.clone_repo(local_repo, "no-such-branch")
    assert list(scratch.iterdir()) == []


def test_run_tests_reports_pass_and_fail(tmp_path):
    (tmp_path / "test_a.py").write_text("def test_ok():\n    assert True\n")
    passed, _ = runner.run_tests(str(tmp_path), sys.executable)
    assert passed

    (tmp_path / "test_b.py").write_text("def test_broken():\n    assert 1 == 2\n")
    passed, output = runner.run_tests(str(tmp_path), sys.executable)
    assert not passed
    assert "test_broken" in output


def test_run_tests_stops_at_the_timeout(tmp_path):
    (tmp_path / "test_slow.py").write_text("import time\n\ndef test_slow():\n    time.sleep(10)\n")
    passed, output = runner.run_tests(str(tmp_path), sys.executable, timeout=2)
    assert not passed
    assert "longer than 2 seconds" in output
