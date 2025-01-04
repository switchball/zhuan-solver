from state.node import Node

# 示例用法
class ExampleNode(Node):
    def __init__(self, state, from_action=None):
        super().__init__(state, from_action)

    def is_goal(self):
        # 示例：当状态为 'goal' 时为终点状态
        return self.state == 'goal'

    def get_neighbors(self):
        # 示例：根据当前状态生成邻居节点及其对应的动作
        neighbors_with_actions = []
        if self.state == 'start':
            neighbors_with_actions.append((ExampleNode('A', 'Action1'), 'Action1'))
            neighbors_with_actions.append((ExampleNode('B', 'Action2'), 'Action2'))
        elif self.state == 'A':
            neighbors_with_actions.append((ExampleNode('C', 'Action3'), 'Action3'))
        elif self.state == 'B':
            neighbors_with_actions.append((ExampleNode('D', 'Action4'), 'Action4'))
        elif self.state == 'C':
            neighbors_with_actions.append((ExampleNode('goal', 'Action5'), 'Action5'))
        elif self.state == 'D':
            neighbors_with_actions.append((ExampleNode('goal', 'Action6'), 'Action6'))
        return neighbors_with_actions

    def get_priority(self):
        # 示例：定义简单的优先级规则，可以根据实际情况调整
        priorities = {
            'start': (0, -5),
            'A': (0, -4),
            'B': (0, 3),
            'C': (0, 2),
            'D': (0, 1),
            'goal': (-1, -1)
        }
        return priorities.get(self.state, float('inf'))
