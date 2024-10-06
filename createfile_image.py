import my_modules.getinfo
import os, time

urls = my_modules.getinfo.geturls("old_data/urls.txt")

cnt = 0
for url in urls:
    code = my_modules.getinfo.getcode(url)
    link = my_modules.getinfo.getpageurl(code)
    links = my_modules.getinfo.getimageurl(link)

    for i in range(0,len(links)):
        url = links[i]
        os.system("curl "+url+" > "+os.path.join('images\\', '{}_{}.jpg'.format(code,i)))
        cnt += 1