from aip import AipOcr

# https://blog.csdn.net/coder_pig/article/details/79417035


# 新建一个AipOcr对象
config = {
    'appId': '11315890',
    'apiKey': 'mwZGy4hnXmYFVmOyVOtDEcaC',
    'secretKey': 'nFBeRaVxFnGjHybxgu09BkGsQZuGnhL4'
}
client = AipOcr(**config)


# 读取图片
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


# 识别图片里的文字
def img_to_str(image_path):
    image = get_file_content(image_path)
    # 调用通用文字识别, 图片参数为本地图片
    # result = client.basicGeneral(image)

    """ 如果有可选参数 """
    options = dict()
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    result = client.basicGeneral(image, options)

    """ 调用通用文字识别（高精度版） """
    # result = client.basicAccurate(image)

    """ 调用网络图片文字识别, 图片参数为本地图片 """
    # result = client.webImage(image)

    # 结果拼接返回
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])


if __name__ == '__main__':
    print(img_to_str('./codeimage/youxiu.gif'))
