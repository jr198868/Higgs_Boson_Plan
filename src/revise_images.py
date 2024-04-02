from PIL import Image

def revise_images(image_path):
    # 打开图片
    image = Image.open(image_path)
    width = 787 #1400  # 固定宽度
    height = 1400 #787  # 固定高度

    # 计算缩放比例
    original_width, original_height = image.size
    scale = min(width / original_width, height / original_height)

    # 计算缩放后的大小
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # 缩放图片
    image = image.resize((new_width, new_height))

    # 创建新的画布
    canvas = Image.new('RGB', (width, height), (0, 0, 0))

    # 计算居中位置
    x = (width - new_width) // 2
    y = (height - new_height) // 2

    # 将缩放后的图片粘贴到画布上
    canvas.paste(image, (x, y))

    # 保存图片
    canvas.save(image_path)