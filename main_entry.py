import numpy as np
import random

from PIL import Image

from app.zhuan.board_state import BoardState
from app.zhuan.zhuan_node import ZhuanNode
from app.zhuan.zhuan_recognizer import YOLORecognizer, ZhuanRecognizer
from app.zhuan.zhuan_react import ZhuanReact

from controller.common_controller import CommonController
from state.search import BFS, GBFS


def random_state():
    # 生成 [1, 2, ..., 10] * 4
    base_list = list(range(1, 42)) * 2
    
    # 添加若干个 0，直到总共有 140 个数字
    num_zeros = 140 - len(base_list)
    if num_zeros < 0:
        raise ValueError("The base list already exceeds 140 elements.")
    
    base_list.extend([0] * num_zeros)
    
    # 打乱列表
    random.shuffle(base_list)
    
    # 重塑为 14x10 的矩阵
    result = np.array(base_list).reshape(14, 10)
    
    return result

def from_image_state():
    rec = YOLORecognizer('runs/classify/train/weights/best.pt')
    board_image = Image.open("images/image.png")
    return rec.recognize(board_image)

def zhuan_rec():
    rec = ZhuanRecognizer('runs/classify/train/weights/best.pt')
    full_image = Image.open("images/screenshot.png")
    return rec.recognize(full_image)

def entry_from_local_image():
    # 旧的入口函数，从本地图片启动测试
    initial_state = [
        [0, 1, 2, 3, 4, 5, 6, 7, 2, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 9, 8],
        [0, 0, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    initial_state = random_state()

    initial_state = from_image_state()[0]

    zhuan_result = zhuan_rec()
    print(zhuan_result)
    initial_state = zhuan_result.result
    # neighbors = test_node.get_neighbors()

    start_node = ZhuanNode(BoardState(initial_state))

    gbfs = GBFS(start_node)
    path = gbfs.search()
    if path:
        print("找到路径:")
        for node in path:
            print(node.from_action)
    else:
        print("未找到路径")
    gbfs.show_algorithm_stats()


if __name__ == "__main__":
    controller = CommonController(config={
        "window_title": "砖了个砖",
        "recognizer": ZhuanRecognizer('runs/classify/train2/weights/best.pt'),
        "react": ZhuanReact(),
        "fps": 4,
        "frame_max_running": 1500
    })

    controller.main_loop()
