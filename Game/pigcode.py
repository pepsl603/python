from PIL import Image, ImageOps, ImageDraw

import pytesseract

# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-ORC\\tesseract.exe'


def get_bin_table(threshold=140):
    # 获取灰度转二值的映射table
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


# 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
# 该函数也可以改成RGB判断的,具体看需求如何
def getPixel(image, x, y, G, N):
    L = image.getpixel((x, y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x, y - 1))
    else:
        return None

    # 降噪


# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, G, N, Z):
    draw = ImageDraw.Draw(image)

    for i in range(0, Z):
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)


try:
    print('开始识别...')
    im = Image.open('./codeimage/6.png')

    # im = im.convert('L')  # 转化为灰度图
    # table = get_bin_table(140)
    # im = im.point(table, '1')

    table = get_bin_table(140)
    im = im.convert('L')
    binaryImage = im.point(table, '1')
    im1 = binaryImage.convert('L')
    im2 = ImageOps.invert(im1)
    im3 = im2.convert('1')
    im4 = im3.convert('L')
    # # 将图片中字符裁剪保留
    box = (10, 2, 165, 25)
    region = im4.crop(box)
    # 将图片字符放大
    im = region.resize((330, 46))

    # 将图片转换成灰度图片
    im = im.convert("L")
    # 去噪,G = 50,N = 4,Z = 4
    clearNoise(im, 50, 4, 3)

    im.load()
    im.show()
    # lang = 'chi_sim+equ+eng'
    aa = pytesseract.image_to_string(im, lang='chi_sim+equ+eng')

    print('输出：', aa)
except Exception as ex:
    print(ex)
