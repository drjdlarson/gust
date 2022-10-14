import setuptools

extras = {'linux': ["gunicorn>=20.1.0"]}
setuptools.setup(
    name="gust",
    version="1.0.0",
    description="GCS for UAS Swarming and Teaming (GUST).",
    long_description="",
    url="https://github.com/drjdlarson/gust/",
    author="Laboratory for Autonomy GNC and Estimation Research (LAGER)",
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
        "pillow"
    ],
    include_package_data=True,
    zip_safe=False,
)
