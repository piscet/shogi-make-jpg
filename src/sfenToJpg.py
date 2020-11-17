# param
import config as cnf
import info
from load_sfen import ParseSfen
from make_txt_image import Piece_IMG

# other
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageOps

class MakeJpg:
    def __init__(self, sfen, turn=None):
        self.sfen = ParseSfen(sfen)
        self.init_param()
        self.piece_img = Piece_IMG(self.mass_size)
        self.make_board()
        self.set_piece()
        self.set_hand()

    def init_param(self):
        self.board_size = tuple(
            num - num % 9 for num in cnf.board_size
        )   # 9の倍数に設定しておく。
        # 升目の大きさの情報
        self.mass_size_height = self.board_size[0] // 9
        self.mass_size_width  = self.board_size[1] // 9
        self.mass_size = self.mass_size_width, self.mass_size_height

        # 駒は升目の真ん中に（木村一基九段）
        self.mass_center_height = self.mass_size_height // 2
        self.mass_center_width = self.mass_size_width // 2

        self.space = cnf.space
        self.hand_ratio = .9
        self.hand_space = 10

        # 駒台の情報
        self.hand_size = self.hand_size_width, self.hand_size_height = (
            int(self.mass_size_width * self.hand_ratio + 2 * self.hand_space),
            int(self.mass_size_height * self.hand_ratio * 7 + 2 * self.hand_space),
        )

        # 駒台についての位置や大きさについて
        self.hand_mass_size_height = int(self.mass_size_height * self.hand_ratio)
        self.hand_mass_size_width = int(self.mass_size_width * self.hand_ratio)

        self.jpg_size = self.jpg_size_width, self.jpg_size_height = (
            self.board_size[1] + self.hand_size_width * 2 + self.space * 2,
            self.board_size[0] + self.space * 2,
        )

        # 盤面の左上の座標の設定
        self.board_coord_width  = self.space + self.hand_size_width
        self.board_coord_height = self.space

        # 駒台の左上の座標の設定
        # black
        self.hand_coord_black = (
            self.hand_coord_width_black,
            self.hand_coord_height_black,
        ) = (
            self.jpg_size_width - self.space - self.hand_size_width,
            self.jpg_size_height - self.space - self.hand_size_height,
        )

        # white
        self.hand_coord_white = (
            self.hand_coord_width_white,
            self.hand_coord_height_white,
        ) = self.space, self.space

        # ボードの線の太さ
        self.bold = cnf.bold

    def make_board(self):
        self.board = Image.new("L", self.jpg_size[::], "white")
        self.draw = ImageDraw.Draw(self.board)
        self.add_line()

    def add_line(self):
        # 盤面
        for i in range(10):
            # 横
            self.draw.line(
                (
                    self.board_coord_width,
                    self.space + i * self.mass_size_height,
                    self.jpg_size_width-self.board_coord_width,
                    self.space + i * self.mass_size_height,
                ),
                fill=(0),
                width=self.bold
            )
            # 縦
            self.draw.line(
                (
                self.board_coord_width + i * self.mass_size_width,
                self.board_coord_height,
                self.board_coord_width + i * self.mass_size_width,
                self.jpg_size_height - self.space,
                ),
                fill=(0),
                width=self.bold
            )

        # 駒台
        # brack
        hand_size_coord_black = (
            self.jpg_size_width - self.space,
            self.jpg_size_height - self.space
        )

        self.draw.rectangle(
            hand_size_coord_black + self.hand_coord_black,
            outline=(0),
            width = 3
        )

        # white
        hand_size_coord_white = (
            self.space + self.hand_size_width,
            self.space + self.hand_size_height
        )

        self.draw.rectangle(
            hand_size_coord_white + self.hand_coord_white,
            outline=(0),
            width = 3
        )

        # font
        self.font = ImageFont.truetype(info.font_pth, info.font_size_number)


    def set_piece(self):
        # 盤面に駒を並べる
        for coord, turn, isGrade, piece in self.sfen:
            print(coord, turn, isGrade, piece)
            self.write_piece(coord, turn, isGrade, piece)

    def write_piece(self, coord, turn, isGrade, piece):
        count_h, count_w = coord
        img = self.piece_img.get_img(piece, turn, isGrade)

        # 特定の位置に駒を表示させる。
        pos = (
            self.board_coord_width + count_w * self.mass_size_width,
            self.board_coord_height + count_h * self.mass_size_height,
        )
        self.board.paste(img, pos, ImageOps.invert(img))

    def set_hand(self):
        # 持ち駒を並べる
        for turn, hand in enumerate(self.sfen.info.hand):
            for pos, piece in enumerate(hand):
                self.write_piece_hand(piece, hand[piece], turn, pos)

    def write_piece_hand(self, piece, num, turn, count_pos):
        init_pos = (
            self.hand_coord_black if turn else self.hand_coord_white
        )
        if turn:
            pos = (
                init_pos[0] + self.hand_space//2,
                init_pos[1] + self.hand_space//2 + self.hand_mass_size_height * count_pos
            )
        else:
            pos = (
                init_pos[0] + self.hand_space//2,
                init_pos[1] + self.hand_space//2 + self.hand_mass_size_height * (6 - count_pos)
            )
        img = self.piece_img.get_img(piece, turn, False)
        self.board.paste(img, pos, ImageOps.invert(img))
        # 数字の表示
        num = str(num)
        w, h = self.draw.textsize(num, font = self.font)
        num_pos = (
            pos[0] + self.hand_mass_size_width - w // 2,
            pos[1] + self.hand_mass_size_height - h // 2 - 2
        )
        self.draw.text(
            num_pos, num, font = self.font, fill = (0), outline = (255)
        )

    def output(self, name=None):
        self.board.save('result.jpg')


if __name__ == "__main__":
    # test = 'sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'
    test = 'lnsg4l/4k1+B2/p1pppp2p/6pb1/7P1/2P4r1/P2PPPP1P/2S1K2S1/+r2G1G1NL b S2N2Pglp 1'
    board = MakeJpg(test)
    plt.imshow(board.board)
    plt.show()
    board.output()
    print(board.sfen.info.hand)
    # import pdb; pdb.set_trace()