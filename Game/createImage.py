from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random


def getRandomColor():
    '''获取一个随机颜色(r,g,b)格式的'''
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return (c1, c2, c3)


def createimg_by_name(name):
    # 获取一个Image对象，参数分别是RGB模式。宽150，高30，随机颜色
    image = Image.new('RGB', (256, 256), getRandomColor())

    # 获取一个画笔对象，将图片对象传过去
    draw = ImageDraw.Draw(image)

    # 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
    font = ImageFont.truetype("simhei.ttf", size=250)

    # 在图片上写东西,参数是：定位，字符串，颜色，字体
    draw.text((70, 5), name[0].upper(), getRandomColor(), font=font)

    image.show()
    small_image = image.resize((40, 40), Image.ANTIALIAS)
    small_image.show()


createimg_by_name('htet')


# # 获取一个Image对象，参数分别是RGB模式。宽150，高30，随机颜色
# image = Image.new('RGB', (40, 40), getRandomColor())
# # image.show()
# # 获取一个画笔对象，将图片对象传过去
# draw = ImageDraw.Draw(image)
#
# # 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
# font = ImageFont.truetype("simhei.ttf", size=32)
#
# # 在图片上写东西,参数是：定位，字符串，颜色，字体
# draw.text((3, 3), '黄', getRandomColor(), font=font)
#
# # 保存到硬盘，名为test.png格式为png的图片
# # image.save(open('test.png', 'wb'), 'png')
# image.show()


