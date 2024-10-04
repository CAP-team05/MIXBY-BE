import my_modules.getinfo
import os, glob

urls = my_modules.getinfo.geturls("old_data/urls.txt")

cnt = 0
fs = glob.glob('images_merged/*_merged.jpg')
for url in urls:
    code = my_modules.getinfo.getcode(url)
    f = glob.glob('images_merged/{}_merged.jpg'.format(code))
    #print(f)

print('merged images found {} out of {}'.format(len(fs), len(urls)))