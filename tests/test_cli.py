import pytest
from typer.testing import CliRunner
from gitch.cli import app

runner = CliRunner()

def test_commit_help():
    result = runner.invoke(app, ["commit", "--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "commit" in result.output

def test_commit_no_message():
    result = runner.invoke(app, ["commit"])
    assert result.exit_code != 0
    assert "Missing option '--m'" in result.output

def test_commit_with_message(monkeypatch):
    # Monkeypatch subprocess and post_devlog so we don't actually commit or open a browser
    import gitch.core

    monkeypatch.setattr("gitch.core.subprocess.run", lambda *a, **kw: None)
    monkeypatch.setattr("gitch.core.subprocess.check_output", lambda *a, **kw: b"file1.py\nfile2.py\n")
    monkeypatch.setattr("gitch.core.post_devlog", lambda title, body: print(f"MOCK POST: {title}\n{body}"))

    result = runner.invoke(app, ["commit", "-m", "Test commit"])
    assert result.exit_code == 0
    assert "Test commit" in result.output or "MOCK POST" in result.output
