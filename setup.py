from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Linedrive",
    version="1.0.2",
    description="A Python client for interacting with ESPN's Gamecast service. Follow gameplay events at the command line.",
    long_description=long_description,
    url="https://github.com/PoorBillionaire/linedrive",
    author="Adam Witt",
    author_email="accidentalassist@gmail.com",
    license="Apache Software License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires=">=3",
    keywords="NBA WNBA NCAA NCAAM NCAAW NHL NFL ESPN Gamecast",
    packages=find_packages(),
    install_requires=["requests", "websocket-client"],
    entry_points={
        "console_scripts":["linedrive.py=src.cli:main"]
    }
)
