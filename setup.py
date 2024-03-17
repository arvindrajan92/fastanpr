import os
import subprocess
from setuptools import setup, find_packages

VERSION = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
    .lstrip("v.")
)

if "-" in VERSION:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = VERSION.split("-")
    VERSION = v + "+" + i + ".git." + s

assert "-" not in VERSION
assert "." in VERSION

assert os.path.isfile("fastanpr/version.py")
with open("fastanpr/version.py", "w", encoding="utf-8") as fh:
    fh.write(f"__version__ = \"{VERSION}\"")

VERSION = "0.1.3"
DESCRIPTION = 'A fast automatic number-plate recognition (ANPR) library'
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="fastanpr",
    version=VERSION,
    author="arvindrajan92 (Arvind Rajan)",
    author_email="<arvindrajan92@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'': ['*.pt'], 'fastanpr': ['*.pt']},
    include_package_data=True,
    install_requires=['ultralytics>=8.1.26', 'paddlepaddle>=2.6.0', 'paddleocr>=2.7.0.3'],
    python_requires='>=3.8',
    extras_require={
        'dev': ['pytest', 'pytest-asyncio', 'twine', 'python-Levenshtein', 'setuptools', 'wheel', 'twine', 'flake8']
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/arvindrajan92/fastanpr',
    keywords=[
        'python', 'anpr', 'fast', 'licence plate', 'number plate', 'detection', 'recognition', 'YOLOv8', 'paddleocr',
        'paddlepaddle'
    ]
)
