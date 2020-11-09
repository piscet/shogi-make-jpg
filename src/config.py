import user_settings as usr
import info

board_size = (usr.board_size, int(usr.board_size * info.ratio))
jpg_size = tuple(num + usr.space * 2 for num in board_size)

space = usr.space
bold = usr.bold

hand_ratio = info.hand_ratio
hand_space = info.hand_space

print(f"board_size = {board_size}")
print(f"jpg_size = {jpg_size}")
print(f"bold = {bold}")