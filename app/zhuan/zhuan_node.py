from app.zhuan.board_state import BoardState
from state.node import Node


class ZhuanNode(Node):
    def __init__(self, board_state: BoardState, from_action=None):
        self.state = board_state
        self.from_action = from_action

    def is_goal(self):
        """
        判断当前节点是否为终点状态。
        
        :return: 如果是终点状态返回 True，否则返回 False
        """
        for row in self.state.tiles:
            if any(tile != 0 for tile in row):
                return False
        return True

    def get_neighbors(self):
        """
        获取从当前节点出发可以到达的所有邻居节点。
        
        :return: 返回一个包含 (邻居节点, 动作) 的列表
        """
        neighbors_with_actions = []
        state_set = set()
        all_moves = self.state.available_moves()
        for start, end, search_dir_key in all_moves:
            new_state = self.state.apply_move_copy(start, end, search_dir_key)
            # new state 判重
            new_board_state = BoardState(new_state)
            if new_board_state not in state_set:
                state_set.add(new_board_state)
                neighbors_with_actions.append(
                    (ZhuanNode(new_board_state, (start, end, search_dir_key)), (start, end, search_dir_key))
                )

        return neighbors_with_actions

    def get_priority(self):
        """
        计算并返回当前节点的优先级。
        
        :return: 返回节点的优先级值，数值越小优先级越高
        """
        return -self.state.elimated_tiles()

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)
