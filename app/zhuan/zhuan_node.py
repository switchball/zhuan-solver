from app.zhuan.board_state import BoardState
from state.node import Node


class ZhuanNode(Node):
    def __init__(self, board_state, from_action=None):
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
        return []
        raise NotImplementedError("get_neighbors 方法需要在子类中实现")

    def get_priority(self):
        """
        计算并返回当前节点的优先级。
        
        :return: 返回节点的优先级值，数值越小优先级越高
        """
        return 0

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __lt__(self, other):
        return self.state< other.state