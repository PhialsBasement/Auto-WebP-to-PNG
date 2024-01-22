# Automatic WebP to PNG Converter

WebP to PNG Converter is a Python script that monitors the downloads folder for newly downloaded WebP files, converts them to PNG using an API, and replaces the original files.

## Features

- Automatically converts newly downloaded WebP files to PNG.
- Monitors the downloads folder for changes every 5 seconds.
- Uses the Flask API to perform the conversion.

## Prerequisites

- Python 3.x
- Pillow library
- Flask library
- Watchdog library

Install the required dependencies using the following command:

```bash
pip install Pillow Flask watchdog
```
# USAGE

1. Clone the repo
```bash
git clone https://github.com/PhialsBasement/Auto-WebP-to-PNG/
```
2. cd into the directory
```bash
cd Auto-WebP-to-PNG
```
3. Run the Flask API
```bash
python API.py
```
4. Run the watchdog
```bash
python main.py
``` 
