from collections import deque
from .search import GBFS

class Node:
    def __init__(self, state, from_action=None):
        """
        初始化节点对象。
        
        :param state: 节点的状态表示
        :param from_action: 可选参数，表示到达该节点的动作
        """
        self.state = state
        self.from_action = from_action

    def is_goal(self):
        """
        判断当前节点是否为终点状态。
        
        :return: 如果是终点状态返回 True，否则返回 False
        """
        raise NotImplementedError("is_goal 方法需要在子类中实现")

    def get_neighbors(self):
        """
        获取从当前节点出发可以到达的所有邻居节点。
        
        :return: 返回一个包含 (邻居节点, 动作) 的列表
        """
        raise NotImplementedError("get_neighbors 方法需要在子类中实现")

    def get_priority(self):
        """
        计算并返回当前节点的优先级。
        
        :return: 返回节点的优先级值，数值越小优先级越高
        """
        raise NotImplementedError("get_priority 方法需要在子类中实现")

    def __eq__(self, other):
        """重载等于运算符，仅根据状态进行比较"""
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        """重载 hash 方法，使节点可以作为字典或集合的键"""
        return hash(self.state)

    def __repr__(self):
        """返回节点的字符串表示形式，便于调试和打印"""
        action_str = f" via {self.from_action}" if self.from_action else ""
        return f"Node(\n{self.state}{action_str})"

    def __lt__(self, other):
        """重载小于运算符，用于优先队列中的比较"""
        return self.get_priority() < other.get_priority()



