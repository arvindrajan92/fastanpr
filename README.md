# FastANPR
A fast automatic number-plate recognition (ANPR) library. This package employs YOLOv8, a lightweight model, for detection, and Paddle OCR, a lightweight *optical character recognition* (OCR) library.

## Installation
```bash
pip install fastanpr
```

## Usage
```python
import cv2
import asyncio

from fastanpr import FastANPR

# To use cuda, replace 'cpu' with 'cuda' or device id, e.g., '0'. Default is set to 'cpu'.
fast_anpr = FastANPR(device='cpu')

files = [...]

for file in files:
    image = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB)
    anpr_result = asyncio.run(fast_anpr.run(image))
    print(anpr_result)
```

## Licence
This project incorporates the YOLOv8 model from Ultralytics, which is licensed under the AGPL-3.0 license. As such, this project is also distributed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE) to comply with the licensing requirements.

For more details on the YOLOv8 model and its license, please visit the [Ultralytics GitHub repository](https://github.com/ultralytics/ultralytics).

## Contributing

We warmly welcome contributions from the community! If you're interested in contributing to this project, please start by reading our [CONTRIBUTING.md](CONTRIBUTING.md) guide.

Whether you're looking to submit a bug report, propose a new feature, or contribute code, we're excited to see what you have to offer. Please don't hesitate to reach out by opening an issue or submitting a pull request.

Thank you for considering contributing to our project. Your support helps us make the software better for everyone.