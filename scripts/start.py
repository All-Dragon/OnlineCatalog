import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_compose(*arguments: str) -> None:
    subprocess.run(
        ["docker", "compose", *arguments],
        cwd=PROJECT_ROOT,
        check=True,
    )


def main() -> None:
    run_compose("config", "--quiet")

    run_compose(
        "up",
        "--build",
        "--wait",
        "--wait-timeout",
        "120",
    )

    run_compose(
        "exec",
        "-T",
        "--index",
        "1",
        "bot",
        "python",
        "manage_webhook.py",
        "set",
    )


if __name__ == "__main__":
    main()