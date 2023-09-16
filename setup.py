"""setup.py for pytest_houdini."""
# Standard Library
from pathlib import Path

# Third Party
from setuptools import find_packages, setup

# Package meta-data.
NAME = "pytest-houdini"
DESCRIPTION = "pytest plugin for testing code in Houdini."
URL = "https://github.com/captainhammy/pytest-houdini"
AUTHOR = "Graham Thompson"
AUTHOR_EMAIL = "captainhammy@gmail.com"
REQUIRES_PYTHON = ">=3.7.0"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name=NAME,
    use_scm_version=True,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=("tests",)),
    install_requires=[
        "pytest",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
            "pytest-datadir",
            "pytest-mock",
            "tox",
        ]
    },
    entry_points={
        "pytest11": ["pytest-houdini = pytest_houdini.plugin"],
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Framework :: Pytest",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Testing",
    ],
)
