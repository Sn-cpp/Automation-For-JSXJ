# Automation For JSXJ
## Description
An Open-CV and Tesseract-OCR based script for automating tasks in the Swordsman([Kiếm Thế](https://kiemthe.vnggames.com/)) game by Kingsoft and VNG.

## Requirements
- Install Tesseract-OCR engine from its [GitHub repository](https://github.com/tesseract-ocr/tessdoc) and add it to the PATH configuration.
- Import the Conda environment from the [jxsj.yml](jsxj.yml) file.

## Running the script
In the console with activated environment, run:
````
python main.py
````

## Notes
- If you encounter a ImportError with `win32api`, try to reinstall it using
````
pip install pywin32
```` 
