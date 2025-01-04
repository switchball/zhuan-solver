from app.zhuan.board_state import BoardState
from app.zhuan.zhuan_node import ZhuanNode
from state.search import BFS, GBFS

if __name__ == "__main__":
    start_node = ZhuanNode(BoardState())
    gbfs = GBFS(start_node)
    path = gbfs.search()
    if path:
        print("找到路径:")
        for node in path:
            print(node)
    else:
        print("未找到路径")