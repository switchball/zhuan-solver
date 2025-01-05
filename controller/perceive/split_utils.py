from PIL import Image

def split_image(image_obj: Image, rows, cols):
    """
    读取图像并将其分割为指定行数和列数的小图片。
    如果不能均匀分割，舍弃余数部分。
    
    :param image_obj: 图像
    :param rows: 分割后的行数
    :param cols: 分割后的列数
    :return: 分割后的小图片列表
    """

    # 打开图像
    img = image_obj
    width, height = img.size

    # 计算每个小图片的宽度和高度
    tile_width = width // cols
    tile_height = height // rows

    # 舍弃余数部分
    new_width = tile_width * cols
    new_height = tile_height * rows
    img = img.crop((0, 0, new_width, new_height))

    # 分割图像
    tiles = []
    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height
            tile = img.crop((left, upper, right, lower))
            tiles.append(tile)

    return tiles

def crop_image(image_obj: Image, xywhn: tuple):
    """
    根据归一化后的坐标和尺寸裁剪图像。
    
    :param image_obj: 原始图像
    :param xywhn: 归一化后的坐标和尺寸 (x, y, w, h)
    :return: 裁剪后的图像
    """
    # 解包归一化后的坐标和尺寸
    x, y, w, h = xywhn

    # 获取图像的原始尺寸
    width, height = image_obj.size

    # 计算实际的坐标和尺寸
    left = int(x * width)
    upper = int(y * height)
    right = int((x + w) * width)
    lower = int((y + h) * height)

    # 裁剪图像
    cropped_image = image_obj.crop((left, upper, right, lower))

    return cropped_image
