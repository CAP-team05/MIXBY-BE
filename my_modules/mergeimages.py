import glob, os
from PIL import Image

def combineImage(full_width,full_height,code,image_list,index):
    canvas = Image.new('RGB', (full_width, full_height), 'white')
    output_height = 0
    
    for im in image_list:
        width, height = im.size
        canvas.paste(im, (0, output_height))
        output_height += height

    canvas.save('images_merged//'+code+'_merged.jpg')

def listImage(image_key,files):
    full_width, full_height,index = 0, 0, 1
    image_list = []
    
    for f in files:
        im = Image.open(f)
        width, height = im.size

        if full_height+height > 65000:
            combineImage(full_width,full_height,image_key,image_list,index)
            index = index + 1
            image_list = []
            full_width, full_height = 0, 0
        
        image_list.append(im)
        full_width = max(full_width, width)
        full_height += height

    combineImage(full_width,full_height,image_key,image_list,index)

def getimagelist(code):
    files = glob.glob('images/{}_*.jpg'.format(code))
    files.sort()
    listImage(code, files)