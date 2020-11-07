"""CLI entry point for proj-template."""

import os
import sys
import yaml

from proj_template.proj_template import create_project


def usage():
    """Display program usage."""
    exe = os.path.basename(sys.argv[0])
    print("usage: %s [-h] [-R] project_cfg" % exe)
    print("\nCreates the basic structure for a Python project.")
    print("\nArguments:")
    print("    project_cfg    project description file")
    print("\nOptions:")
    print("    -h, --help     display this help message")
    print("    -R, --no-root  don't create root directory, use current one.")


def main():
    """Program entry point."""
    config_file = 0
    create_root = True
    for opt in sys.argv[1:]:
        if opt in ["-h", "--help"]:
            usage()
            sys.exit(0)
        elif opt in ["-R", "--no-root"]:
            create_root = False
        else:
            if bool(config_file):
                print("EROR: Can only create one project.")
                usage()
                sys.exit(1)
            config_file = opt
    with open(config_file, "r") as yaml_file:
        cfg_data = yaml.safe_load(yaml_file)
        cfg_data["__create_root"] = create_root
        create_project(cfg_data)


if __name__ == "__main__":
    main()
