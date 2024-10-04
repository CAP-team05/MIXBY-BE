import glob, pytesseract

# tesseract 가 윈도우 지원이 깔끔해서 윈도우로 해야할듯???

cnt = 0
fs = glob.glob('images_merged/*_merged.jpg')
for f in fs[:5]:
    text = pytesseract.image_to_string(f, lang='kor+eng')
    print(text)