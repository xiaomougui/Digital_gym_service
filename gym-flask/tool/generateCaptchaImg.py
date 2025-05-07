import random
import string
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def generate_captcha_image_base64():
    # 生成随机验证码（4位字母数字）
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # 图片尺寸
    width, height = 120, 40

    # 创建白色背景图片
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 加载字体（默认或指定字体）
    try:
        font = ImageFont.truetype("arial.ttf", size=24)
    except:
        font = ImageFont.load_default()

    # 绘制验证码文本（随机颜色）
    for i, char in enumerate(captcha_text):
        draw.text(
            (10 + i * 25, 5),
            char,
            fill=(random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)),
            font=font
        )

    # 添加干扰线
    for _ in range(3):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)),
                  width=1)

    # 添加噪点
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # 转换为 Base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return captcha_text, img_base64