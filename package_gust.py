import argparse
import subprocess
import re
import os
import sys

from typing import Tuple
from pathlib import Path


DOCKER_INFO_FILE = "/workspaces/gust/src/build/settings/base.json"


def define_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Automatically package GUST and create an installer"
    )

    choices = ("major", "minor", "patch")
    p.add_argument(
        "type",
        type=str,
        help="Type of release to perform",
        choices=choices,
    )

    p.add_argument(
        "-s",
        "--skip-increment",
        action="store_true",
        help="Flag indicating if incrementing the version should be skipped. "
        + "If this is passed then the type is irrelevant.",
    )
    
    return p


def get_match(line: str):
    return re.search('"version\s*":\s*"(\d+).(\d+).(\d+)"', line)


def get_version() -> Tuple[int, int, int]:
    with open(DOCKER_INFO_FILE, "r") as fin:
        for line in fin:
            matched = get_match(line)
            if matched:
                major = int(matched.groups()[0])
                minor = int(matched.groups()[1])
                patch = int(matched.groups()[2])
                return major, minor, patch

    raise RuntimeError("Failed to extract version from {:s}".format(DOCKER_INFO_FILE))


def set_version(major: int, minor: int, patch: int):
    tmp_file = DOCKER_INFO_FILE + ".tmp"
    with open(DOCKER_INFO_FILE, "r") as fin:
        with open(tmp_file, "w") as fout:
            for line in fin:
                matched = get_match(line)
                if matched:
                    ind = line.find('"')
                    new_line = line[:ind] + '"version": "{:d}.{:d}.{:d}",\n'.format(
                        major, minor, patch
                    )
                    fout.write(new_line)
                else:
                    fout.write(line)

    os.replace(tmp_file, DOCKER_INFO_FILE)


if __name__ == "__main__":
    
    args = define_parser().parse_args()

    major, minor, patch = get_version()
    print("Current version: {:d}.{:d}.{:d}".format(major, minor, patch))

    # setting the new version number
    if not args.skip_increment:
        if args.type == "major":
            major += 1
            minor = 0
            patch = 0
        elif args.type == "minor":
            minor += 1
            patch = 0
        elif args.type == "patch":
            patch += 1
        else:
            raise RuntimeError("Invalid type: {} should not be here".format(args.type))

        set_version(major, minor, patch)
    else:
        print("Skipping incrementing of version number!")

    version_str = "v{:d}.{:d}.{:d}".format(major, minor, patch)
    print("Releasing version: {:s}".format(version_str[1:]))

    # running the release_gust script
    # this packages the software and creates a .deb
    print("Packaging GUST using fbs...\n\n")
    cmd_str = "cd ./build_scripts && ./release_gust.bash"
    subprocess.run(cmd_str, shell=True)

    print("")
    print("\n\n Package Created. GUST is ready to be deployed. Exit the docker container and run deploy_gust.py script to deploy the docker image.")


