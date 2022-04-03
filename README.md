# partReader
A Python script to read part numbers from technical drawings (.tiff) and append them to .txt files for each tech. drawing

### Environment
* Win10 (But it may work w/Linux too)
* Python3+
* [Tesseract](https://github.com/tesseract-ocr/tesseract#installing-tesseract) needs to be installed beforehand.
* Pip

### Deployment
After installing Tesseract, 
```bash
pip install requirements.txt
```

### Usage 
1. Put *.tiff* files into ```~\drawings``` 
folder.
1. From command line interface, run the script.
1. it will return *.txt* files which contain the part numbers. 

### Notes:
* _This will not work with Part numbers which include letters._
* The part number handling schema is specific to one use case. (Part number needs to be in XX.XXXXX-XXXX format)
* This can be changed with changing the script's ```regex``` portions.


