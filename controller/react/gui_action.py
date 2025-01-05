

class GUIAction:
    """所有交互动作的基类"""

    def execute(self, coords):
        raise NotImplementedError

    def normalize_to_window_coords(self, coords, x: float, y: float):
        """
        将归一化后的坐标 (x, y) 转换为窗口内的实际坐标。

        :param coords: 窗口坐标 (left, top, width, height)
        :param x: 归一化后的 x 坐标 (0 到 1)
        :param y: 归一化后的 y 坐标 (0 到 1)
        :return: 窗口内的实际坐标 (window_x, window_y)
        """
        left, top, width, height = coords
        window_x = left + int(x * width)
        window_y = top + int(y * height)
        return window_x, window_y
