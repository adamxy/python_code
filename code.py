#encoding=utf-8
from flask import Flask
import StringIO
import random
import string
from PIL import Image,ImageDraw,ImageFont,ImageFilter

app = Flask(__name__)

class Code(object):
    def __init__(self):
        self.filename = "./"
        self.font_path = './simhei.ttf' #字体文件路径
        self.number = 4 #生成几位数的验证码
        self.size = (129,53) #生成验证码图片的高度和宽度
        self.bgcolor = (255,255,255) #背景颜色，默认为白色
        self.fontcolor = (0,0,0) #字体颜色，默认为蓝色
        self.linecolor = (0,0,0) #干扰线颜色。默认为红色
        self.draw_line = True #是否要加入干扰线
        self.line_number = (2,5) #加入干扰线条数的上下限

    #用来随机生成一个字符串
    def gene_text(self):
        source  = string.printable[:62]
        # source = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G',
        # 'H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','X','Z']
        return ''.join(random.sample(source,self.number))#number是生成验证码的位数

    #用来绘制干扰线
    def gene_line(self,draw,width,height):
        # begin = (random.randint(0, width), random.randint(0, height))
        # end = (random.randint(0, width), random.randint(0, height))
        begin = (0, random.randint(0, height))
        end = (74, random.randint(0, height))
        draw.line([begin, end], fill = self.linecolor,width=3)

    #生成验证码
    def gene_code(self):
        width,height = self.size #宽和高
        image = Image.new('RGBA',(width,height),self.bgcolor) #创建图片
        font = ImageFont.truetype(self.font_path,40) #验证码的字体
        draw = ImageDraw.Draw(image)  #创建画笔
        text = self.gene_text() #生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / self.number, (height - font_height) / self.number),text,\
                font= font,fill=self.fontcolor) #填充字符串
        if self.draw_line:
            self.gene_line(draw,width,height)
        # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
        # 图形扭曲参数
        #image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
        return image, text

@app.route("/code")
def index():
    code = Code()
    image, text = code.gene_code()
    buf = StringIO.StringIO()
    image.save(buf, 'jpeg', quality=100)
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=1111)
