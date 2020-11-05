from PIL import Image 
  
img = Image.open('flag.png')
w, h = img.size
print(w, h)

newimg = Image.new(mode = "RGB", size = (w, h // 10))

for y in range(7, h, 10):
    for x in range(w):
        pixel = img.getpixel((x, y))
        newimg.putpixel((x, y // 10), pixel)

newimg.save('flag_out.png')
