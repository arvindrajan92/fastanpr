from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A fast automatic number-plate recognition (ANPR) library'
LONG_DESCRIPTION = ('A package that employs lightweight models (such as YOLO) and library (such as Paddle OCR) for a '
                    'fast ANPR')

setup(
    name="fastanpr",
    version=VERSION,
    author="arvindrajan92 (Arvind Rajan)",
    author_email="<arvindrajan92@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['ultralytics>=8.1.26', 'paddlepaddle>=2.6.0', 'paddleocr>=2.7.0.3'],
    python_requires='>=3.9',
    license='MIT',
    keywords=['python', 'anpr', 'fast', 'licence plate', 'detection', 'recognition', 'yolo']
)
