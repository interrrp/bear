#!/usr/bin/env python

# Bear 0.1.0 - Python 3.11+ - https://github.com/interrrp/bear - MIT License
# If you are not contributing to Bear, you should not be modifying this file.

import platform
import subprocess
from pathlib import Path
from sys import argv, exit
from typing import Callable
from venv import EnvBuilder

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
VENV_PATH = Path(".venv")


def venv() -> int:
    log("creating virtual environment")
    builder = EnvBuilder(with_pip=True)
    builder.create(VENV_PATH)
    log(f"created virtual environment at {VENV_PATH}\n")

    sync()

    log("activate the virtual environment with:")
    log(f"  linux (bash): source {VENV_PATH}/bin/activate")
    log(f"  windows (cmd): {VENV_PATH}/Scripts/activate.bat")
    log(f"  windows (powershell): ./{VENV_PATH}/Scripts/activate.ps1\n")

    log("done")

    return EXIT_SUCCESS


def sync() -> int:
    log("installing requirements")
    install_requirements()
    log("installed requirements\n")

    log("done")

    return EXIT_SUCCESS


COMMANDS: dict[str, Callable[[], int]] = {
    "venv": venv,
    "sync": sync,
}


def install_requirements() -> None:
    pip_args = ["install", "-r", "requirements.txt"]

    if platform.system() == "Windows":
        pip_path = VENV_PATH / "Scripts" / "pip.exe"
    else:
        pip_path = VENV_PATH / "bin" / "pip"

    subprocess.run([pip_path, *pip_args], check=True)


def main() -> int:
    if len(argv) < 2:
        log("no command specified")
        show_available_commands()
        return EXIT_FAILURE

    command = argv[1]
    if command not in COMMANDS:
        log(f"unknown command: {command}")
        show_available_commands()
        return EXIT_FAILURE

    return COMMANDS[command]()


def show_available_commands() -> None:
    log(f"available commands: {', '.join(COMMANDS.keys())}")


def log(message: str = "") -> None:
    print(f"bear: {message}")


if __name__ == "__main__":
    exit(main())
