from click.testing import CliRunner

from aiotasks.actions.cli import cli


def test_parser_cli_runs_ok():
    runner = CliRunner()
    result = runner.invoke(cli, ["-h"])

    assert result.exit_code == 0
