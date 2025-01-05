import math

from app.zhuan.board_state import BoardState
from app.zhuan.zhuan_node import ZhuanNode
from app.zhuan.zhuan_constants import (
    BOARD_AREA_POSITION,
    NUM_BOARD_ROWS,
    NUM_BOARD_COLS,
)

from controller.recognize.maybe_result import MaybeResult
from controller.react.mouse_action import NoAction, ClickAction, DragAction
from state.search import GBFS


class ZhuanReact:
    def __init__(self):
        self._cache_path = None

    def run_planning_search(self, start_node):
        gbfs = GBFS(start_node)
        path = gbfs.search()
        gbfs.show_algorithm_stats()
        return path

    def react(self, result: MaybeResult):
        if result.prob < 0.8:
            print("识别置信度低于 0.8 跳过响应")
            return NoAction()
        
        initial_state = result.result
        start_node = ZhuanNode(BoardState(initial_state))

        # if self._cache_path is not None:
        #     print("使用缓存路径")
        #     path = self._cache_path
        #     self._cache_path = None
        #     return path

        path = self.run_planning_search(start_node)
        if path is None:
            print("未找到路径")
            return NoAction()
        else:
            self._cache_path = path
        
        # 获取路径的第二个节点的来源动作 （第一个节点是起点）
        action_step = path[1].from_action
        print(f"规划动作: {action_step}")

        normalized_action = self.build_action(action_step)
        print(f"归一化动作: {normalized_action}")
        return normalized_action

    def build_action(self, action_step):
        # format: ((start_row, start_col), (end_row, end_col), dir)
        start, end, _dir = action_step  

        if start == end:
            # click action
            return ClickAction(*self._board_pos_to_full_pos(*start))
        else:
            # drag action
            distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
            end_fix = (
                end[0] + math.copysign(0.4, end[0] - start[0]),
                end[1] + math.copysign(0.4, end[1] - start[1]),
            )  # 往终点坐标移动方向多偏离若干的像素
            return DragAction(
                *self._board_pos_to_full_pos(*start), 
                *self._board_pos_to_full_pos(*end_fix),
                duration=0.1 + distance * 0.1
            )

    def _board_pos_to_full_pos(self, row_idx, col_idx):
        # 将 [棋盘坐标] 转换为 [归一化的相对屏幕坐标] 
        local_x = (col_idx + 0.5) / NUM_BOARD_COLS
        local_y = (row_idx + 0.5) / NUM_BOARD_ROWS
        x, y, w, h = BOARD_AREA_POSITION
        return x + w * local_x, y + h * local_y
