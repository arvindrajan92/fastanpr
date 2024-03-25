import os
import sys
import subprocess
from setuptools import setup, find_packages

# Getting build version
try:
    VERSION = (
        subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
        .lstrip("v.")
    )

    if "-" in VERSION:
        v, i, s = VERSION.split("-")
        VERSION = v + "+" + i + ".git." + s

    assert "-" not in VERSION
    assert "." in VERSION

    assert os.path.isfile("fastanpr/version.py")
    with open("fastanpr/version.py", "w", encoding="utf-8") as fh:
        fh.write(f"__version__ = \"{VERSION}\"\n")

except Exception:
    with open("fastanpr/version.py", "r", encoding="utf-8") as fh:
        VERSION = fh.read().strip().lstrip("__version__ = \"").rstrip("\"")

# Set Python version requirements based on the operating system
if sys.platform.startswith('win'):
    PYTHON_REQUIRES = '>=3.8, <3.11'
else:
    PYTHON_REQUIRES = '>=3.6'

# Getting long description from README
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="fastanpr",
    version=VERSION,
    author="arvindrajan92 (Arvind Rajan)",
    author_email="<arvindrajan92@gmail.com>",
    description='A fast automatic number-plate recognition (ANPR) library',
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'': ['*.pt'], 'fastanpr': ['*.pt']},
    include_package_data=True,
    install_requires=['ultralytics>=8.1.34', 'paddlepaddle>=2.6.1', 'paddleocr>=2.7.2'],
    python_requires=PYTHON_REQUIRES,
    extras_require={
        'dev': ['pytest', 'pytest-asyncio', 'twine', 'python-Levenshtein', 'setuptools', 'wheel', 'twine', 'flake8']
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/arvindrajan92/fastanpr',
    keywords=[
        'python', 'anpr', 'fast', 'licence plate', 'number plate', 'detection', 'recognition', 'YOLOv8', 'paddleocr',
        'paddlepaddle'
    ]
)
