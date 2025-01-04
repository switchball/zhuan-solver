from app.example.example_node import ExampleNode
from state.search import GBFS, BFS


if __name__ == "__main__":
    start_node = ExampleNode('start')
    gbfs = GBFS(start_node)
    path = gbfs.search()
    if path:
        print("找到路径:")
        for node in path:
            print(node)
    else:
        print("未找到路径")