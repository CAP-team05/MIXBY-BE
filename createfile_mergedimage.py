import my_modules.mergeimages
import my_modules.getinfo

import json

urls = my_modules.getinfo.geturls("old_data/urls.txt")
print(len(urls))

cnt = 0
errors = []
for url in urls:
    #print(url)
    code = my_modules.getinfo.getcode(url)
    try:
        images = my_modules.mergeimages.getimagelist(code)
    except:
        print('error!', url)
        errors.append(my_modules.getinfo.getpageurl(code))
        cnt += 1

with open('errorurls.json', 'w', encoding='utf-8') as f:
    json.dump(errors, f, ensure_ascii = False, indent=4)

print("total error {} out of {}".format(cnt, len(urls)))