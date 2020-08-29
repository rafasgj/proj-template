"""CLI entry point for pyproject."""

import sys
import yaml
from datetime import datetime
import os
import os.path

from pyproject.pyproject import (
    build_copying,
    build_setup_cfg,
    create_project_dirs,
)


def main(*args):
    """Program entry point."""
    config_file = args[0] if args else 0
    with open(config_file, "r") as yaml_file:
        cfg_data = yaml.safe_load(yaml_file)
    cfg_data["year"] = datetime.now().strftime("%Y")
    tgt_dir = cfg_data["project"]["name"]
    create_project_dirs(tgt_dir)
    cfg_data["license_classifier"] = build_copying(tgt_dir, cfg_data)
    with open(os.path.join(tgt_dir, "setup.py"), "wt") as setup_py:
        print("import setuptools\n\nsetuptools.setup()", file=setup_py)
    with open(os.path.join(tgt_dir, "version.txt"), "wt") as version:
        print(cfg_data["project"].get("version", "0.0.1"), file=version)
    build_setup_cfg(tgt_dir, cfg_data)


if __name__ == "__main__":
    main(*(sys.argv[1:]))
