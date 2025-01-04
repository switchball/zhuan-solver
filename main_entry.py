import numpy as np
import random

from app.zhuan.board_state import BoardState
from app.zhuan.zhuan_node import ZhuanNode
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

if __name__ == "__main__":
    initial_state = [
        [0, 1, 2, 3, 4, 5, 6, 7, 2, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 9, 8],
        # ... 其他行 ...
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
    
    # neighbors = test_node.get_neighbors()

    start_node = ZhuanNode(BoardState(initial_state))
    print(start_node)
    import time 
    time.sleep(3)
    gbfs = GBFS(start_node)
    path = gbfs.search()
    if path:
        print("找到路径:")
        for node in path:
            print(node)
    else:
        print("未找到路径")
    gbfs.show_algorithm_stats()