import sys
sys.path.append('src')
from sfenToJpg import MakeJpg
demo_txt = 'lnsg4l/4k1+B2/p1pppp2p/6pb1/7P1/2P4r1/P2PPPP1P/2S1K2S1/+r2G1G1NL b S2N2Pglp 1'

print(sys.argv)
if len(sys.argv) < 2:
    raise Exception("sfenが選択されていません")

if sys.argv[1] == 'demo':
    sfen = demo_txt
    name = 'demo_result'
else:
    sfen = sys.argv[1]
    name = 'test'

board = MakeJpg(sfen)
board.show()
board.output(name)