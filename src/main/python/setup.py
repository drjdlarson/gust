import setuptools
import json
import os
import pathlib

with open(os.path.join(pathlib.Path(__file__).parent.resolve(), "..", "..", "build", "settings", "base.json")) as fin:
    settings = json.load(fin)

extras = {'linux': ["gunicorn>=20.1.0"]}
setuptools.setup(
    name=settings["app_name"],
    version=settings["version"],
    description="GCS for UAS Swarming and Teaming (GUST).",
    long_description="",
    url="https://github.com/drjdlarson/gust/",
    author=settings["author"],
    author_email="",
    license="GPL",
    packages=setuptools.find_packages(),
    install_requires=[
        "flask==2.0.2",
        "flask-restx==0.5.1",
        "requests",
        "pyqt5",
        "werkzeug==2.0.3",
        "pyserial",
        "pyinstaller>=4.9",
        "matplotlib",
        "scipy",
        "pillow",
        "dronekit",
        "pyqtgraph",
    ],
    include_package_data=True,
    zip_safe=False,
)
