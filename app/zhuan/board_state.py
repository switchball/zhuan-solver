

class BoardState:
    def __init__(self, initial_state=None):
        """
        初始化 BoardState 对象。
        
        :param initial_state: 可选参数，用于初始化棋盘的状态。
                               如果为 None，则初始化为空棋盘。
        """
        self.rows = 14
        self.cols = 10
        if initial_state is None:
            # 初始化为空棋盘
            self.tiles = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            self.tiles = tuple(tuple(row) for row in self.tiles)
        else:
            # 使用给定的初始状态进行初始化
            if len(initial_state) != self.rows or any(len(row) != self.cols for row in initial_state):
                raise ValueError("initial_state 的尺寸必须为 14x10")
            self.tiles = initial_state

    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        """
        返回 BoardState 对象的哈希值。
        
        :return: 哈希值
        """
        return hash(self.tiles)

    def __repr__(self):
        """返回棋盘的字符串表示形式，便于调试和打印"""
        return '\n'.join([' '.join(map(str, row)) for row in self.tiles])



if __name__ == "__main__":
    # 创建一个空棋盘
    board = BoardState()
    board2 = BoardState()

    assert board == board2

    # 创建一个带有初始状态的棋盘
    initial_state = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # ... 其他行 ...
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    ]
    board_with_initial_state = BoardState(initial_state)
    print(board_with_initial_state)