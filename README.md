![Word to TXT](https://img.shields.io/badge/Version-0.1-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

# Word2TXT
Having trouble copying text from PDF? No problem, Word2TXT app will help you extract text from images.

## Features
- Word to Images: Important feature. You should start with it first
- JPEG to PNG: Not important feature, but it will be useful if you want to convert JPEG to PNG
- OCR Images: Central feature. It will export images to text for you to copy and paste into Word. Supported 2 modes:
+ Fast: Export fast thanks to your CPU. For desktops, I recommend 4 CPUs. For laptops, I recommend 2 CPUs or less
+ Slow: Slower but more efficient mode. I recommend this mode for laptops, or for desktops too

## Installations
### 1. Download `Tesseract OCR`
- [Windows](https://github.com/tesseract-ocr/tesseract)
- MacOS:
```bash
brew install tesseract
```
- Linux:
```bash
sudo apt install tesseract-ocr
```

### 2. Install languages
- Windows: Go to [Tessdata](https://github.com/tesseract-ocr/tessdata) and install language you want or all languages
- MacOS:
```bash
brew install tesseract-lang
```
- Linux:
```bash
sudo apt install tesseract-ocr-all
```

Also, you can install language types from:
- Best: https://github.com/tesseract-ocr/tessdata_best
- Fast: https://github.com/tesseract-ocr/tessdata_fast

### 3. Use the application
You have 2 methods to use the application:
- Download from [Releases](https://github.com/WMZS-Modding/Word2TXT/releases)
- Clone repository:
```bash
git clone https://github.com/WMZS-Modding/Word2TXT.git
```

And then run:
```bash
python main.py
```

### 4. Usage
- First, you need to convert your PDF to DOCX. I recommend using `Gooogle Drive` and `Gooogle Docs`
- Second, click the application you've downloaded and extracted
- Then, choose the `Word2PNG` section. Choose your input DOCX and output folder. In the `JPEG2PNG` section, it's optional but it's good for you if you prefer PNG instead of JPEG
- Next, choose the `OCR Images` section. I recommend choosing `Slow` mode to get a better result. Choose your language in `Language` part (*Languages will automatically show after you paste* `traineddata` (*Windows*) *or install language* (*MacOS and Linux*)). Choose your input image folder and output TXT folder. In `Fast` mode, I recommend choosing 4 CPU
- Finally, check your output TXT folder, you'll see result

## Advantages and Disadvantages
### Fast
- Advantages: Runs on CPU. Can process large image folders. Gives fast results
- Disadvantages: Sometimes this mode is too "rushed" leading to skimming and giving results that are almost missing some words
### Slow
- Advantages: Processes image folders very carefully. Gives more accurate results
- Disadvantages: Slow and can take a long time to process large image folders. With 128 images or more, the time will increase

## Contributing
- Fork this repository
- Make your own changes
- Send a pull request for me