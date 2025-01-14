import math
import time

from app.zhuan.board_state import BoardState
from app.zhuan.zhuan_node import ZhuanNode
from app.zhuan.zhuan_constants import (
    BOARD_AREA_POSITION,
    NUM_BOARD_ROWS,
    NUM_BOARD_COLS,
    EACH_TILE_CONFIDENCE,
)

from controller.recognize.maybe_result import MaybeResult
from controller.react.mouse_action import NoAction, ClickAction, DragAction
from state.search import GBFS


class ZhuanReact:
    def __init__(self):
        self._cache_path = None
        self._total_prob_thres = EACH_TILE_CONFIDENCE ** (NUM_BOARD_ROWS * NUM_BOARD_COLS)
        self._missing_cache_wait_max = 5
        self._missing_cache_wait_crt = 0
        self._cache_hit_idx = 0

    def run_planning_search(self, start_node):
        gbfs = GBFS(start_node)
        path = gbfs.search()
        gbfs.show_algorithm_stats()
        if gbfs._stats_visited_state > 10000:
            t = start_node.state.tiles
            a = [[int(u) for u in x]for x in t]
            print((a), "State.Tiles")
            if path is not None:
                for node in path:
                    print(node.from_action)
            # exit()
        return path

    def react(self, result: MaybeResult):
        if result.prob < self._total_prob_thres:
            print(f"识别置信度低于 {self._total_prob_thres:.3f} 跳过响应 prob = {result.prob}")
            return NoAction()
        
        initial_state = result.result
        start_node = ZhuanNode(BoardState(initial_state))

        path = None
        if self._cache_path is not None:
            if start_node in self._cache_path:
                idx = self._cache_path.index(start_node)
                path = self._cache_path[idx:]
                print(f"从缓存中读取路径位于 {idx} of {len(path)}")
                self._missing_cache_wait_crt = 0
                self._cache_hit_idx = 0
            else:
                print("路径不在缓存中")
                self._missing_cache_wait_crt += 1
                self._cache_hit_idx += 1
                if self._missing_cache_wait_crt < self._missing_cache_wait_max:
                    if self._cache_hit_idx + 1 < len(self._cache_path):
                        action_step = self._cache_path[self._cache_hit_idx + 1].from_action
                        print(f"  从缓存中读取路径位于 {self._cache_hit_idx} of {len(self._cache_path)}")
                        return self.build_action(action_step)
                    return NoAction()
                elif self._missing_cache_wait_crt == self._missing_cache_wait_max:
                    print("  等待 1s")
                    time.sleep(1)
                    return NoAction()
                self._missing_cache_wait_crt = 0

        if path is None:
            path = self.run_planning_search(start_node)
        if path is None:
            print("未找到路径")
            return NoAction()
        else:
            self._cache_path = path
        
        # 获取路径的第二个节点的来源动作 （第一个节点是起点）
        if len(path) < 2:
            print("已经到达终点")
            return NoAction()
        action_step = path[1].from_action
        print(f"规划动作: {action_step}")

        normalized_action = self.build_action(action_step)
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
