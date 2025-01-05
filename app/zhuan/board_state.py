from app.zhuan.zhuan_constants import NUM_BOARD_ROWS, NUM_BOARD_COLS


class BoardState:
    def __init__(self, initial_state=None):
        """
        初始化 BoardState 对象。
        
        :param initial_state: 可选参数，用于初始化棋盘的状态。
                               如果为 None，则初始化为空棋盘。
        """
        self.rows = NUM_BOARD_ROWS
        self.cols = NUM_BOARD_COLS
        if initial_state is None:
            # 初始化为空棋盘
            self.tiles = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            # 使用给定的初始状态进行初始化
            if len(initial_state) != self.rows or any(len(row) != self.cols for row in initial_state):
                raise ValueError("initial_state 的尺寸必须为 14x10")
            self.tiles = initial_state
        # 确保为 tuple 不可变类型
        self.tiles = tuple(tuple(row) for row in self.tiles)

        self._projected_tiles = None
        self._scan_moves = 0

    def elimated_tiles(self):
        """返回棋盘上已消除的方块的数量"""
        return sum(row.count(0) for row in self.tiles)

    def available_moves(self):
        """返回棋盘上可用的移动位置列表"""
        if self._projected_tiles is None:
            self._projected_tiles = self._compute_projected_board()

        moves = []
        scan_moves = 0
        for row_idx in range(self.rows):
            line_moves = self._available_moves_by_line(self.tiles[row_idx])
            scan_moves += len(line_moves)
            for (col_start, col_end) in line_moves:
                # pick pattern at (row_idx, col_start)
                # ptn = self.tiles[row_idx][col_start]

                # search pattern in _projected_tiles at (row_idx, col_end)
                if dir_key := self.check_single_move((row_idx, col_start), (row_idx, col_end), True):
                    moves.append(((row_idx, col_start), (row_idx, col_end), dir_key))

        reflected_tiles = tuple(zip(*self.tiles))
        for col_idx in range(self.cols):
            line_moves = self._available_moves_by_line(reflected_tiles[col_idx])
            scan_moves += len(line_moves)
            for (row_start, row_end) in line_moves:
                # pick pattern at (row_start, col_idx)
                # ptn = reflected_tiles[col_idx][row_start]

                # search pattern in _projected_tiles at (row_end, col_idx)
                if dir_key := self.check_single_move((row_start, col_idx), (row_end, col_idx), False):
                    moves.append(((row_start, col_idx), (row_end, col_idx), dir_key))
    
        self._scan_moves = scan_moves
        return moves

    def apply_move_copy(self, start: tuple, end: tuple, search_dir_key: str) -> list:
        """
        根据给定的移动，返回执行后的棋盘状态。
        
        :param start: 移动的起始位置
        :param end: 移动的目标位置
        :param search_dir_key: 移动的方向字符串
        :return: 更新后的棋盘状态
        """
        row_start, col_start = start
        row_end, col_end = end
        tiles_copy = list(list(row) for row in self.tiles)

        # 计算搜索方向向量 search_dir
        if search_dir_key == 'right':
            search_dir = [0, 1]
        elif search_dir_key == 'left':
            search_dir = [0, -1]
        elif search_dir_key == 'up':
            search_dir = [-1, 0]
        elif search_dir_key == 'down':
            search_dir = [1, 0]
        else:
            raise ValueError("Invalid search direction key")

        # 计算移动方向向量 move_dir
        move_dir_row = row_end - row_start
        move_dir_col = col_end - col_start

        if move_dir_row == 0 and move_dir_col > 0:
            move_dir = [0, 1]  # right
        elif move_dir_row == 0 and move_dir_col < 0:
            move_dir = [0, -1]  # left
        elif move_dir_row > 0 and move_dir_col == 0:
            move_dir = [1, 0]  # down
        elif move_dir_row < 0 and move_dir_col == 0:
            move_dir = [-1, 0]  # up
        elif move_dir_row == 0 and move_dir_col == 0:
            move_dir = [0, 0]  # no move
        else:
            raise ValueError("Invalid direction")
            
        # 计算移动的步数
        steps = abs(move_dir_row) if move_dir_row != 0 else abs(move_dir_col)

        # 沿着 move_dir 搜索直到遇到第一个为0的 tile
        queue = 0
        if steps > 0:
            current_row, current_col = row_start, col_start
            while 0 <= current_row < len(tiles_copy) and 0 <= current_col < len(tiles_copy[0]):
                if tiles_copy[current_row][current_col] == 0:
                    break
                current_row += move_dir[0]
                current_col += move_dir[1]
                queue += 1

        # 移动 tile，逆序覆盖
        for i in reversed(range(queue)):
            tiles_copy[row_end + i * move_dir[0]][col_end + i * move_dir[1]] = tiles_copy[row_start + i * move_dir[0]][col_start + i * move_dir[1]]
            tiles_copy[row_start + i * move_dir[0]][col_start + i * move_dir[1]] = 0

        # 获取 end 坐标的 tile pattern 值
        end_tile_pattern = tiles_copy[row_end][col_end]

        # 消除 end 的 tile
        tiles_copy[row_end][col_end] = 0

        # 沿着 search_dir 的方向搜索，跳过若干可能的 0，直到遇到第一个非0的 tile
        search_row, search_col = row_end, col_end
        while 0 <= search_row < len(tiles_copy) and 0 <= search_col < len(tiles_copy[0]):
            if tiles_copy[search_row][search_col] != 0:
                break
            search_row += search_dir[0]
            search_col += search_dir[1]

        # 检查是否找到非0的 tile
        if not (0 <= search_row < len(tiles_copy) and 0 <= search_col < len(tiles_copy[0])):
            raise ValueError("No non-zero tile found in the specified search direction")

        # 获取找到的非0 tile 的 pattern 值
        found_tile_pattern = tiles_copy[search_row][search_col]

        # 检查 pattern 是否一致
        if end_tile_pattern == found_tile_pattern:
            tiles_copy[row_end][col_end] = 0  # 消除 end 的 tile
            tiles_copy[search_row][search_col] = 0  # 消除找到的 tile
        else:
            raise ValueError("Pattern mismatch, cannot eliminate tile")

        return tiles_copy

    def check_single_move(self, start: tuple, end: tuple, horizontal: bool):
        """
        检查给定的移动能否消除棋盘棋子
        
        :param start: 移动的起始位置
        :param end: 移动的目标位置
        :param horizontal: 是否为水平移动
        :return: 如果移动能消除棋子，返回方向字符串；否则返回 False。
        """
        row_start, col_start = start
        row_end, col_end = end
        ptn = self.tiles[row_start][col_start]
        if ptn == 0:
            return False
        if horizontal:
            keys = ["up", "down"]  # 水平移动，则只检测垂直方向，下同
        else:
            keys = ["left", "right"]
        for key in keys:
            pt = self._projected_tiles[key]
            if ptn == pt[row_end][col_end]:
                a = 1
                return key
        return False


    def _compute_projected_board(self):
        """
        计算当前棋盘状态向上下左右4个方向的可消除版本。
        
        :return: 4 个 tiles 2D 数组，其中每个元素表示一个方向上的可消除版本。
        """
        left, right = self._compute_projected_board_sub(self.tiles)
        up, down = self._compute_projected_board_sub(tuple(zip(*self.tiles)))
        up = tuple(zip(*up))
        down = tuple(zip(*down))
        return {
            "left": left,
            "right": right,
            "up": up,
            "down": down,
        }

    def _compute_projected_board_sub(self, tiles):
        """
        计算当前棋盘状态向左右2个方向的可消除版本。
        
        :return: 2 个 tiles 2D 数组，其中每个元素表示一个方向上的可消除版本。
        """
        result_left = []
        for row in tiles:
            out = [0] + list(row[0:-1])
            for idx in range(1, len(out)):
                if out[idx] == 0:
                    out[idx] = out[idx - 1]
            result_left.append(out)
        
        result_right = []
        for row in tiles:
            out = list(row[1:]) + [0]
            for idx in reversed(range(len(out) - 1)):
                if out[idx] == 0:
                    out[idx] = out[idx + 1]
            result_right.append(out) 

        return result_left, result_right

        # return [self.tiles,  # 原始棋盘
        #         self.tiles[::-1],  # 反转后的棋盘
        #         tuple(zip(*self.tiles)),  # 旋转后的棋盘
        #         tuple(zip(*self.tiles))[::-1]]  # 反转并旋转后的棋盘

    def _available_moves_by_line(self, line_elements: list) -> list:
        """
        返回给定行列上所有的移动位置列表。
        
        :param line_elements: 一条的数据数组 
        :return: 可用移动位置列表 [(start_idx, end_idx), ...]
        """
        n = len(line_elements)
        left_moves = [0] * n
        right_moves = [0] * n
        
        # 第一次扫描：计算每个 tile 可以向左或向右移动的最大数目
        left_zero_index = -1
        left_zero_eof = -1
        left_crt_moves = 0
        right_zero_index = n
        right_zero_eof = n
        right_crt_moves = 0
        
        for i in range(n):
            # 计算向左移动的最大步数
            if line_elements[i] != 0:
                left_moves[i] = left_crt_moves
                left_zero_eof = i
            else:
                left_zero_index = i
                left_crt_moves = left_zero_eof - left_zero_index
            
            # 计算向右移动的最大步数
            j = n - 1 - i
            if line_elements[j] != 0:
                right_moves[j] = right_crt_moves
                right_zero_eof = j
            else:
                right_zero_index = j
                right_crt_moves = right_zero_eof - right_zero_index

        # 第二次扫描：根据向左向右最大格数生成 move pairs
        moves = []
        for i in range(n):
            if line_elements[i] != 0:
                # 向左/右移动，包括移动0格
                for step in range(left_moves[i], right_moves[i] + 1):
                    moves.append((i, i + step))
        
        return moves


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

    t = board.elimated_tiles()
    m = board.available_moves()

    # 创建一个带有初始状态的棋盘
    initial_state = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    board_with_initial_state = BoardState(initial_state)
    print(board_with_initial_state)

    t = board_with_initial_state.elimated_tiles()
    m = board_with_initial_state.available_moves()

    for move in m:
        new_state = board_with_initial_state.apply_move_copy(*move)
        print(move, "--> \n", "\n".join(map(str, new_state)), "\n\n")

    print(t, m)