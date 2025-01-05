
import pyautogui
import time

from controller.react.gui_action import GUIAction


class NoAction(GUIAction):
    """不执行任何动作"""

    def execute(self, coords):
        pass


class ClickAction(GUIAction):
    def __init__(self, x: float, y: float, delay: float = 0.0, clicks: int = 1, interval: float = 0.0):
        """
        初始化点击操作。

        :param x: 归一化后的 x 坐标 (0 到 1)
        :param y: 归一化后的 y 坐标 (0 到 1)
        :param delay: 操作后的延迟时间（秒）
        :param clicks: 点击次数
        :param interval: 每次点击之间的间隔时间（秒）
        """
        super().__init__()
        self.x = x
        self.y = y
        self.delay = delay
        self.clicks = clicks
        self.interval = interval

    def execute(self, coords):
        """
        执行点击操作。

        :param coords: 窗口坐标 (left, top, width, height)
        """
        window_x, window_y = self.normalize_to_window_coords(coords, self.x, self.y)
        pyautogui.click(window_x, window_y, clicks=self.clicks, interval=self.interval)
        time.sleep(self.delay)

    def __repr__(self):
        return f"ClickAction(x={self.x}, y={self.y}, delay={self.delay}, clicks={self.clicks}, interval={self.interval})"


class DragAction(GUIAction):
    def __init__(self, start_x: float, start_y: float, end_x: float, end_y: float, delay: float = 0.0, duration: float = 0.5):
        """
        初始化拖动操作。

        :param start_x: 起始点的归一化后的 x 坐标 (0 到 1)
        :param start_y: 起始点的归一化后的 y 坐标 (0 到 1)
        :param end_x: 结束点的归一化后的 x 坐标 (0 到 1)
        :param end_y: 结束点的归一化后的 y 坐标 (0 到 1)
        :param delay: 操作后的延迟时间（秒）
        :param duration: 拖动持续时间（秒）
        """
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.delay = delay
        self.duration = duration

    def execute(self, coords):
        """
        执行拖动操作。

        :param coords: 窗口坐标 (left, top, width, height)
        """
        start_x, start_y = self.normalize_to_window_coords(coords, self.start_x, self.start_y)
        end_x, end_y = self.normalize_to_window_coords(coords, self.end_x, self.end_y)
        pyautogui.moveTo(start_x, start_y)
        pyautogui.dragTo(end_x, end_y, duration=self.duration)
        time.sleep(self.delay)

    def __repr__(self):
        return f"DragAction(start_x={self.start_x}, start_y={self.start_y}, end_x={self.end_x}, end_y={self.end_y}, delay={self.delay}, duration={self.duration})"


# 使用示例
if __name__ == "__main__":
    # 假设已经找到了窗口的坐标
    window_coords = (100, 100, 800, 600)  # 窗口坐标 (left, top, width, height)

    # 定义点击操作
    click_action = ClickAction(x=0.5, y=0.5, delay=1.0, clicks=2, interval=0.5)
    click_action.execute(window_coords)

    # 定义拖动操作
    drag_action = DragAction(start_x=0.2, start_y=0.2, end_x=0.8, end_y=0.8, delay=1.0, duration=0.5)
    drag_action.execute(window_coords)