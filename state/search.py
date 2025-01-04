import heapq
from collections import deque


class BFS:
    def __init__(self, start_node):
        """
        初始化 BFS 搜索对象。
        
        :param start_node: 搜索的起始节点
        """
        self.start_node = start_node

    def search(self):
        """
        执行宽度优先搜索。
        
        :return: 如果找到目标节点，返回路径；如果未找到，返回 None
        """
        queue = deque([self.start_node])
        visited = set()
        parent_map = {self.start_node: None}

        while queue:
            current_node = queue.popleft()

            if current_node.is_goal():
                return self._reconstruct_path(current_node, parent_map)

            if current_node in visited:
                continue

            visited.add(current_node)
            neighbors = current_node.get_neighbors()

            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in parent_map:
                    parent_map[neighbor] = current_node
                    queue.append(neighbor)

        return None

    def _reconstruct_path(self, goal_node, parent_map):
        """
        根据父节点映射重构从起点到目标节点的路径。
        
        :param goal_node: 目标节点
        :param parent_map: 父节点映射
        :return: 返回从起点到目标节点的路径
        """
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append(current_node)
            current_node = parent_map[current_node]
        path.reverse()
        return path


class GBFS:
    def __init__(self, start_node):
        """
        初始化 GBFS 搜索对象。
        
        :param start_node: 搜索的起始节点
        """
        self.start_node = start_node

    def search(self):
        """
        执行贪心最佳优先搜索。priority 更小的将被优先搜索。
        
        :return: 如果找到目标节点，返回路径；如果未找到，返回 None
        """
        priority_queue = [(self.start_node.get_priority(), self.start_node)]
        visited = set()
        parent_map = {self.start_node: (None, None)}

        while priority_queue:
            _priority, current_node = heapq.heappop(priority_queue)

            if current_node.is_goal():
                self._stats_visited_state = len(visited)
                return self._reconstruct_path(current_node, parent_map)

            if current_node in visited:
                continue

            visited.add(current_node)
            neighbors_with_actions = current_node.get_neighbors()

            for neighbor, action in neighbors_with_actions:
                if neighbor not in visited and neighbor not in parent_map:
                    parent_map[neighbor] = (current_node, action)
                    heapq.heappush(priority_queue, (neighbor.get_priority(), neighbor))

        self._stats_visited_state = len(visited)

        return None

    def _reconstruct_path(self, goal_node, parent_map):
        """
        根据父节点映射重构从起点到目标节点的路径。
        
        :param goal_node: 目标节点
        :param parent_map: 父节点映射
        :return: 返回从起点到目标节点的路径
        """
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append(current_node)
            current_node, action = parent_map.get(current_node, (None, None))
            if action:
                path[-1].from_action = action  # 更新路径中每个节点的来源动作
        path.reverse()
        return path

    def show_algorithm_stats(self):
        print("visited state num:", self._stats_visited_state)