# 一些常量定义

NUM_BOARD_ROWS = 14  # 棋盘的行数
NUM_BOARD_COLS = 10  # 棋盘的列数

BOARD_AREA_POSITION = (0.05, 0.17, 0.905, 0.7)  # 棋盘主要区域坐标 (x, y, w, h)

# 每个 tile 的置信度，实际置信度为 confidence ** (ROWS * COLS)
EACH_TILE_CONFIDENCE = 0.999

# 是否要保存置信度过低的图片到单独文件夹中
SHOULD_SAVE_LOW_CONF_IMAGES = True