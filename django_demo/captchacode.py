# from openai import OpenAI


# client = OpenAI(
#         api_key="sk-cddgdmfn8xc5pgm2afo5cmfab1rmj50sunw7exxah51niwqs",
#         base_url="https://api.xiaomimimo.com/v1",
#     )

# stream = client.responses.create(
#     model="mimo-v2.6-pro",
#     input="什么是勾股定理?",
#     temperature=0.7,
#     stream=True
# )

# for event in stream:
#     if event.type == "response.output_text.delta":
#         print(event.delta, end="", flush=True)
    
import random
from typing import Tuple
from PIL import ImageFont, Image, ImageDraw
from captcha.image import ImageCaptcha
from io import BytesIO


class CaptchaCode:

    def __init__(self, width, height, spacing=10):
        self.width = width 
        self.height = height 
        self.spacing = spacing 

    def get_captcha_code(self) -> Tuple[BytesIO, str]:
        """获取验证码"""
        # 创建一个 验证码对象 
        captcha = ImageCaptcha(width=self.width, height=self.height, font_sizes=(self.height - 6, ))
        # 随机 生成一个 4位纯数字的验证码 
        chars = "".join(random.choices("0123456789", k=4))
        # 给验证码对象 添加 文字信息 、并返回验证码图片对象
        image = self.create_captcha_with_spacing(captcha, chars, spacing=self.spacing)

        # 给验证码 添加一些 干扰线 
        captcha.create_noise_curve(image, color=(255, 255, 0))
        # 给验证码 添加一些 干扰点
        captcha.create_noise_dots(image, color=(255, 0, 255), number=20)

        out = BytesIO()
        image.save(out, format="png")
        # 将 流的指针指向头部
        out.seek(0)
        return out, chars

    def create_captcha_with_spacing(self, captcha, text, spacing=20):
        width, height = self.width, self.height
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        font_size = random.choice(captcha._font_sizes)
        # 加载字体
        font = ImageFont.truetype('arial.ttf', font_size)
        
        # 计算总宽度
        total_char_width = 0
        char_widths = []
        for char in text:
            # 获取单个字符的边界框
            bbox = draw.textbbox((0, 0), char, font=font)
            char_w = bbox[2] - bbox[0]
            char_widths.append(char_w)
            total_char_width += char_w
        
        # 加上间距后的总宽度
        total_width = total_char_width + (len(text) - 1) * spacing
        
        # 计算起始 X 坐标（居中）
        start_x = (width - total_width) // 2
        start_y = (height - font_size) // 2  # 粗略垂直居中
        
        # 逐个绘制字符
        current_x = start_x
        for i, char in enumerate(text):
            draw.text((current_x, start_y), char, font=font, fill='black')
            # 下一个字符的 X = 当前 X + 当前字符宽度 + 间距
            current_x += char_widths[i] + spacing
        
        return image





