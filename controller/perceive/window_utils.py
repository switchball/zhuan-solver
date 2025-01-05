import pyautogui  # pip install pyautogui
import win32gui  # pip install pywin32
import win32con
import numpy as np


class WindowNotFoundError(Exception):
    """Raised when the window is not found."""
    pass


def find_window_coordinates(window_title):
    """
    查找指定窗口的坐标。
    
    :param window_title: 窗口标题的一部分
    :return: 窗口的坐标 (left, top, width, height)
    """
    def callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if window_title in title:
                rect = win32gui.GetWindowRect(hwnd)
                left, top, right, bottom = rect
                width = right - left
                height = bottom - top
                titles.append((hwnd, left, top, width, height))
        return True

    titles = []
    win32gui.EnumWindows(callback, titles)

    if titles:
        return titles[0][1:]  # 返回第一个匹配窗口的坐标
    return None

def capture_window(window_title, save_screenshot_path=None):
    """
    捕获指定窗口的截图。
    
    :param window_title: 窗口标题的一部分
    :param save_screenshot_path: 如果指定截图保存路径，则保存，默认为 None
    :return: 窗口坐标 (left, top, width, height) 以及 截图 Image 对象
    """
    coords = find_window_coordinates(window_title)
    if coords is None:
        print(f"窗口 '{window_title}' 未找到")
        raise WindowNotFoundError(f"窗口 '{window_title}' 未找到")
        return 

    left, top, width, height = coords

    # 截取屏幕
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    if save_screenshot_path is not None:
        screenshot.save(save_screenshot_path)
        print(f"截图已保存到 {save_screenshot_path}")

    return coords, screenshot

# 使用示例
if __name__ == "__main__":
    window_title = "砖了个砖"  # 微信窗口的部分标题
    output_path = "screenshot.png"
    print(f"正在截取窗口 '{window_title}' 的截图... 延迟 3 秒")
    import time
    time.sleep(3)

    coords, _img = capture_window(window_title, output_path)
    if coords:
        left, top, width, height = coords
        print(f"窗口坐标: 左上角 ({left}, {top}), 宽度 {width}, 高度 {height}")