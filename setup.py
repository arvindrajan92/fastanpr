from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'A fast automatic number-plate recognition (ANPR) library'
LONG_DESCRIPTION = ('A package that employs lightweight models (such as YOLOv8) and library (such as Paddle OCR) for a '
                    'fast ANPR')

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
    python_requires='>=3.9',
    extras_require={'dev': ['pytest>=8.1.1', 'twine>=5.0.0']},
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/arvindrajan92/fastanpr',
    keywords=[
        'python', 'anpr', 'fast', 'licence plate', 'number plate', 'detection', 'recognition', 'YOLOv8', 'paddleocr',
        'paddlepaddle'
    ]
)
