from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random


def get_random_color():
    """
    :return: 获取一个随机颜色(r,g,b)格式
    """
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return (c1,c2,c3)


def createimg_by_name_256(name):
    if name is None or name == '':
        name = 'H'
    # 获取一个Image对象，参数分别是RGB模式。宽256，高256，随机颜色
    image = Image.new('RGB', (256, 256), get_random_color())

    # 获取一个画笔对象，将图片对象传过去
    draw = ImageDraw.Draw(image)

    # 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
    font = ImageFont.truetype("simhei.ttf", size=250)

    # 在图片上写东西,参数是：定位，字符串，颜色，字体
    draw.text((70, 5), name[0].upper(), get_random_color(), font=font)

    # small_image = image.resize((40, 40), Image.ANTIALIAS)

    return image


def get_image_by_size(image, size):
    if image:
        if size > 0:
            return image.resize((size, size), Image.ANTIALIAS)
        else:
            return image
    else:
        # 获取一个Image对象，参数分别是RGB模式。宽256，高256，随机颜色
        default_image = Image.new('RGB', (256, 256), get_random_color())

        # 获取一个画笔对象，将图片对象传过去
        draw = ImageDraw.Draw(default_image)

        # 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
        font = ImageFont.truetype("simhei.ttf", size=250)

        # 在图片上写东西,参数是：定位，字符串，颜色，字体
        draw.text((70, 5), '浪', get_random_color(), font=font)

        if size > 0:
            return image.resize((size, size), Image.ANTIALIAS)
        else:
            return default_image


def get_imgdata(img):
    # 在内存生成图片
    from io import BytesIO
    # f = BytesIO()
    # image.save(f, 'png')
    # data = f.getvalue()
    # f.close()

    with BytesIO() as f:
        img.save(f, 'png')
        data = f.getvalue()
        return data

    return None


if __name__ == '__main__':
    img = createimg_by_name_256('XXX')
    x_img = img
    img1 = get_image_by_size(img, 800)
    img.show()
    img1.show()
