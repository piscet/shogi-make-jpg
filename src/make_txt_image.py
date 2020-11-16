import info
from PIL import Image, ImageDraw, ImageFont, ImageOps

class Piece_IMG:
    def __init__(self, size):
        # 情報の設定
        self.size = size
        self.setup()
        self.load()

    def setup(self):
        # フォントなどの設定
        self.font = ImageFont.truetype(info.font_pth, info.font_size_board)

    def load(self):
        self.black = {}
        self.white = {}
        for key in info.alphToJa:
            txt = info.alphToJa[key]
            img = Image.new("L", self.size, "white")
            draw = ImageDraw.Draw(img)

            h, w = draw.textsize(txt, font=self.font)
            txt_image = Image.new("L", (w, h), (255))
            txt_draw = ImageDraw.Draw(txt_image)
            txt_draw.text((0, 0), txt, font = self.font, fill=(0))

            pos = (
                (self.size[0] - w) // 2,
                (self.size[1] - h) // 2
            )
            img.paste(txt_image, pos)
            self.black[key] = [img]
            self.white[key] = [img.rotate(180, expand=1)]

        for key in info.alphaToJa_nari:
            txt = info.alphaToJa_nari[key]
            img = Image.new("L", self.size, "white")
            draw = ImageDraw.Draw(img)

            h, w = draw.textsize(txt, font=self.font)
            txt_image = Image.new("L", (w, h), (255))
            txt_draw = ImageDraw.Draw(txt_image)
            txt_draw.text((0, 0), txt, font = self.font, fill=(0))

            pos = (
                (self.size[0] - w) // 2,
                (self.size[1] - h) // 2
            )
            img.paste(txt_image, pos)

            self.black[key].append(img)
            self.white[key].append(img.rotate(180, expand=1))

    def get_img(self, piece, turn, isGrade):
        # 画像を出力
        if turn:
            return self.black[piece][isGrade]
        else:
            return self.white[piece][isGrade]

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    img = Piece_IMG((100, 100))
    for piece in info.all_piece:
        plt.imshow(img.get_img(piece, True, False))
        plt.show()
        plt.imshow(img.get_img(piece, False, False))
        plt.show()