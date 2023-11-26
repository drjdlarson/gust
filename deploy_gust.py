"""Automatically build the docker image and push to DockerHub"""
import os
import subprocess
import argparse
import re

from typing import Tuple

VERSION_FILE = os.path.join(os.path.dirname(__file__), "src/build/settings/base.json")
DOCKER_USERNAME = "ualager"
IMAGE_NAME = "gust-lager"
DOCKERFILE_NAME = os.path.join(os.path.dirname(__file__), "dockerfile_deploy")


def define_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Automatically build the docker image and push to DockerHub"
    )

    p.add_argument(
        "-p", "--password", type=str, help="Enter password for lager_gcs@outlook.com"
    )

    return p


def get_match(line: str):
    return re.search('"version\s*":\s*"(\d+).(\d+).(\d+)"', line)


def get_version() -> Tuple[int, int, int]:
    with open(VERSION_FILE, "r") as fin:
        for line in fin:
            matched = get_match(line)
            if matched:
                major = int(matched.groups()[0])
                minor = int(matched.groups()[1])
                patch = int(matched.groups()[2])
                return major, minor, patch

    raise RuntimeError("Failed to extract version from {:s}".format(VERSION_FILE))


if __name__ == "__main__":
    args = define_parser().parse_args()

    # getting the current version to be deployed
    major, minor, patch = get_version()
    version_str = "v{:d}.{:d}.{:d}".format(major, minor, patch)
    print("Current version: {:s}".format(version_str))

    print("Logging into Lager's DockerHub account")
    if args.password is not None:
        cmd_str = "docker login --username={:s} --password={:s}".format(
            DOCKER_USERNAME, args.password
        )
        subprocess.run(cmd_str, shell=True)
    else:
        raise RuntimeError("Provide ualager's DockerHub password to proceed.")

    print("Building the docker image for GUST")
    cmd_str = "docker build -f {:s} -t {:s}/{:s}:{:s} .".format(
        DOCKERFILE_NAME, DOCKER_USERNAME, IMAGE_NAME, version_str
    )
    subprocess.run(cmd_str, shell=True)

    print("Pushing the image to DockerHub")
    cmd_str = "docker push {:s}/{:s}:{:s}".format(
        DOCKER_USERNAME, IMAGE_NAME, version_str
    )
    subprocess.run(cmd_str, shell=True)
