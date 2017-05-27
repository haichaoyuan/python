# PIL:Python Imaging Library，图片处理库

from PIL import Image, ImageFilter
# 1. 处理图片,比如模糊
# 打开一个ipg图像文件，注意是当前路径
print('==========================')
im = Image.open('test.jpg')
# 应用图片模糊
im2 = im.filter(ImageFilter.BLUR)
im2.save('test_blur.jpg', 'jpeg')

print('==========================')
# 生成字母验证码
from PIL import ImageDraw, ImageFont
import random

#随机字母
def rndChar():
    return chr(random.randint(85, 90))

#随机颜色1
def rndColor(lowColor, highColor= 255):
    return (random.randint(lowColor, highColor), random.randint(lowColor, highColor),
            random.randint(lowColor, highColor))

# 240 x 60
width = 60*4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象
font = ImageFont.truetype('/font/simhei.ttf', 42)
# 创建Draw对象
draw = ImageDraw.Draw(image)
# 填充每个像素
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor(64))

#输出文字
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor(32))

# 模糊
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')
