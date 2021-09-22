from PIL import ImageTk, Image, ImageFilter, ImageFont, ImageDraw

def reSizeImage(imagePath, desiredSize):
    img = Image.open(imagePath)
    img2 = img.resize(desiredSize)
    img2 = applyBlur(img2)
    w,h = img.size
    while w > desiredSize[0] or h > desiredSize[1]:
        img = img.resize( (w -int(w/100), h - int(h/100)))
        w,h = img.size
    img2.paste(img, (int((img2.size[0] / 2) - (img.size[0] / 2)) , int((img2.size[1] / 2) - (img.size[1] / 2))))
    fileName = imagePath + '_output.jpg'
    img2.save(fileName)
    return fileName.split('/')[-1]

def applyBlur(image):
    return image.filter(ImageFilter.GaussianBlur(radius = 100))
