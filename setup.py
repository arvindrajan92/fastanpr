import fastanpr
from setuptools import setup, find_packages

VERSION = fastanpr.__version__
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
    python_requires='>=3.8, <3.12',
    extras_require={'dev': ['pytest-asyncio>=0.23.5', 'twine>=5.0.0', 'python-Levenshtein>=0.25.0']},
    license='MIT',
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
