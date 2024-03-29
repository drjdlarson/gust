import setuptools
import json
import os
import pathlib

with open(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "..",
        "..",
        "build",
        "settings",
        "base.json",
    )
) as fin:
    settings = json.load(fin)

extras = {"linux": ["gunicorn>=20.1.0"]}
setuptools.setup(
    name=settings["app_name"],
    version=settings["version"],
    description="GCS for UAS Swarming and Teaming (GUST).",
    long_description="",
    url="https://github.com/drjdlarson/gust/",
    author=settings["author"],
    author_email="lager_gcs@outlook.com",
    license="GPL",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "pyqt5",
        "werkzeug==2.0.3",
        "pyserial",
        "pyinstaller==4.9",
        "scipy",
        "pillow",
        "dronekit",
        "pyqtgraph",
    ],
    include_package_data=True,
    extras_require=extras,
    zip_safe=False,
)
