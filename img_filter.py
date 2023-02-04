import PIL.Image
import pilgram

img = PIL.Image.open("img/img.jpg")

pilgram.lofi(img).save("img/img-filtered.jpg")
