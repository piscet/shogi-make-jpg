# param
import config as cnf

# other
import cv2
import numpy as np
import matplotlib.pyplot as plt

class MakeJpg:
    def __init__(self, sfen, turn=None):
        self.sfen = sfen
        self.init_param()
        self.board = self.make_board()
    
    def init_param(self):
        self.board_size = tuple(
            num - num % 9 for num in cnf.board_size
        )   # 9の倍数に設定しておく。
        # 升目の大きさの情報
        self.mass_size_height = self.board_size[0] // 9
        self.mass_size_width  = self.board_size[1] // 9

        self.space = cnf.space
        self.hand_ratio = .9
        self.hand_space = 10

        # 駒台の情報
        self.hand_size = self.hand_size_height, self.hand_size_width = (
            int(self.mass_size_height * self.hand_ratio * 7 + 2 * self.hand_space),
            int(self.mass_size_width * self.hand_ratio + 2 * self.hand_space),
        )

        self.jpg_size = self.jpg_size_height, self.jpg_size_width = (
            self.board_size[0] + self.space * 2,
            self.board_size[1] + self.hand_size_width * 2 + self.space * 2
        )

        # 盤面の左上の座標の設定
        self.board_coord_width  = self.space + self.hand_size_width
        self.board_coord_height = self.space
        
        # 駒台の左上の座標の設定
        # black
        self.hand_coord_black = (
            self.hand_coord_width_black,
            self.hand_coord_height_black
        ) = (
            self.jpg_size_width - self.space - self.hand_size_width,
            self.jpg_size_height - self.space - self.hand_size_height
        )
        
        # white
        self.hand_coord_white = (
            self.hand_coord_width_white,
            self.hand_coord_height_white
        ) = self.space, self.space

        # ボードの線の太さ
        self.bold = cnf.bold
    
    def make_board(self):
        board = np.ones(self.jpg_size) * 255
        board = self.add_line(board)
        return board
    
    def add_line(self, board):
        # 盤面
        for i in range(10):
            # 横
            board[
                self.space + i * self.mass_size_height: self.space + i * self.mass_size_height + self.bold,
                self.board_coord_width: -self.board_coord_width + self.bold
            ] = 0
            # 縦
            board[
                self.board_coord_height: -self.space + self.bold,
                self.board_coord_width + i * self.mass_size_width: self.board_coord_width + i * self.mass_size_width + self.bold
            ] = 0
        
        # 駒台
        # brack
        hand_size_coord_black = (
            self.jpg_size_width - self.space,
            self.jpg_size_height - self.space
        )
        
        board = cv2.rectangle(
            board,
            self.hand_coord_black,
            hand_size_coord_black,
            0,
            2
        )

        # white
        hand_size_coord_white = (
            self.space + self.hand_size_width,
            self.space + self.hand_size_height
        )
        board = cv2.rectangle(
            board,
            self.hand_coord_white,
            hand_size_coord_white,
            0,
            2
        )
        return board
    
    def output(self, name=None):
        cv2.imwrite('result.jpg', self.board)

    
    
if __name__ == "__main__":
    board = MakeJpg("")
    plt.imshow(board.board, cmap="gray")
    plt.show()
    board.output()