"""CLI entry point for proj-template."""

import sys
import yaml

from proj_template.proj_template import create_project


def main():
    """Program entry point."""
    args = sys.argv[1:]
    config_file = args[0] if args else 0
    with open(config_file, "r") as yaml_file:
        cfg_data = yaml.safe_load(yaml_file)
        create_project(cfg_data)


if __name__ == "__main__":
    main()
