# FastANPR
[![Build Status](https://github.com/arvindrajan92/fastanpr/actions/workflows/push.yaml/badge.svg)

A fast automatic number-plate recognition (ANPR) library. This package employs YOLOv8, a lightweight model, for detection, and Paddle OCR, a lightweight *optical character recognition* (OCR) library.

## Installation
```bash
pip install fastanpr
```

## Usage
```python
import cv2
import time
import asyncio

from typing import List
from fastanpr import FastANPR

async def show_anpr_result(files: List[str]) -> None:
    "Reads image files and sends through fastanpr and reports the processing time taken"
    images = [cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB) for file in files]
    
    start_time = time.time()
    anpr_results = await fast_anpr.run(images)
    end_time = time.time()
    
    for file, anpr_result in zip(files, anpr_results):
        print(file, '\n', anpr_result)
    print(f'{round(end_time-start_time, 4)} s\n')

# To use cuda, replace 'cpu' with 'cuda' or device id, e.g., '0'. Default is set to 'cpu'.
fast_anpr = FastANPR(device='cpu')

# list of image files
files = [...]

# sending images individually
_ = await asyncio.gather(*[show_anpr_result(file) for file in files])

# sending all images at once
result = await show_anpr_result(files)
```

## Licence
This project incorporates the YOLOv8 model from Ultralytics, which is licensed under the AGPL-3.0 license. As such, this project is also distributed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE) to comply with the licensing requirements.

For more details on the YOLOv8 model and its license, please visit the [Ultralytics GitHub repository](https://github.com/ultralytics/ultralytics).

## Contributing

We warmly welcome contributions from the community! If you're interested in contributing to this project, please start by reading our [CONTRIBUTING.md](CONTRIBUTING.md) guide.

Whether you're looking to submit a bug report, propose a new feature, or contribute code, we're excited to see what you have to offer. Please don't hesitate to reach out by opening an issue or submitting a pull request.

Thank you for considering contributing to our project. Your support helps us make the software better for everyone.