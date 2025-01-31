from setuptools import setup

setup(
    name="Pass-Manager",
    version="1.0",
    py_modules=["pass_manager"],  # Name of your main script without .py
    install_requires=[
        "prettytable",  # For displaying data in a formatted table.
        "typer[all]",   # Include Typer for command-line interface.
    ],
    entry_points={
        "console_scripts": [
            "Pass-manager=pass_manager:app",  # Entry point for the command line
        ],
    },
)
