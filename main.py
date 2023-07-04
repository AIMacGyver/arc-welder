#!/usr/bin/env python
"""This module contains functions for running arc-welder.
"""

from pathlib import Path

import click

from arc_welder.pipelines import pipeline


@click.group(context_settings={"auto_envvar_prefix": "FOOP"})
def cli():
    pass


@cli.command()
@click.option("--verbose", is_flag=True, help="Enables verbose mode.")
def run_arc_welder(verbose):
    """
    Runs the arc-welder application.

    Args:
        verbose (bool): Flag indicating whether to run in verbose mode.
    """
    click.echo("Running arc-welder...")
    pipeline(verbose)


if __name__ == "__main__":
    cli()
