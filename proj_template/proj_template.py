"""Create a setup.cfg file from a template."""

import os
from pkg_resources import resource_filename
from urllib.request import urlopen
from datetime import datetime

__main_template = """\"\"\"CLI entry point for proj-template.\"\"\"


def main():
    \"\"\"Program entry point.\"\"\"


if __name__ == "__main__":
    main()
"""

__setup_template = """\"\"\"Setup project.\"\"\"

import setuptools

setuptools.setup()
"""


def create_project(config):
    """Create project."""
    config["year"] = datetime.now().strftime("%Y")
    tgt_dir = config["project"]["name"]
    create_root = config.get("__create_root", True)
    root_dir = tgt_dir if create_root else "."
    create_project_dirs(root_dir, tgt_dir)
    code_dir = os.path.join(root_dir, tgt_dir)
    with open(os.path.join(code_dir, "__main__.py"), "wt") as main_file:
        print(__main_template, end="", file=main_file)
    config["license_classifier"] = build_copying(root_dir, config)
    with open(os.path.join(root_dir, "setup.py"), "wt") as setup_py:
        print(__setup_template, end="", file=setup_py)
    with open(os.path.join(root_dir, "version.txt"), "wt") as version:
        print(config["project"].get("version", "0.0.1"), file=version)
    build_setup_cfg(root_dir, config)


def create_project_dirs(root_dir, target_dir):
    """Create project directories in the target_dir."""
    os.makedirs(os.path.join(root_dir, target_dir), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "tests"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "features/steps"), exist_ok=True)


def build_setup_cfg(root_dir, config_data):
    """Generate a setup.cfg file in the new project directory."""
    filename = resource_filename("proj_template", "/_setup.cfg.in")
    with open(filename, "rt") as infile:
        with open(os.path.join(root_dir, "setup.cfg"), "wt") as outfile:
            print(infile.read().format(**config_data), file=outfile)


def build_copying(root_dir, config_data):
    """Generateproper  COPYING file on target_dir."""
    MIT_license = """
Copyright {year} {author[name]}

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    licenses = {
        "GPLv3": (
            "License :: OSI Approved :: GNU General Public License v3 or later "
            "(GPLv3+)",
            "https://www.gnu.org/licenses/gpl-3.0.txt",
        ),
        "GPLv2": (
            "License :: OSI Approved :: GNU General Public License v2 or later "
            "(GPLv2+)",
            "https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt",
        ),
        "LGPLv3": (
            "License :: OSI Approved :: GNU Lesser General Public License v3 "
            "or later (LGPLv3+)",
            "https://www.gnu.org/licenses/lgpl-3.0.txt",
        ),
        "LGPLv2.1": (
            "License :: OSI Approved :: GNU Lesser General Public License v2.1"
            " or later (LGPLv2.1+)",
            "https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt",
        ),
        "LGPLv2": (
            "License :: OSI Approved :: GNU Lesser General Public License v2.1"
            " or later (LGPLv2.1+)",
            "https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt",
        ),
        "MIT": ("License :: OSI Approved :: MIT License", MIT_license),
    }

    classifier, text = licenses.get(
        config_data["project"].get("license", "GPLv3"), licenses["GPLv3"]
    )
    if text.startswith("http"):
        text = urlopen(text).read()
        if isinstance(text, bytes):
            text = text.decode("utf-8")
    with open(os.path.join(root_dir, "COPYING"), "wt") as license_file:
        print(
            text.format(**config_data), file=license_file,
        )
    return classifier
