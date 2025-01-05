import time
import random

from controller.perceive.window_utils import capture_window
from controller.recognize.base_recognizer import BaseRecognizer
from controller.react.base_react import BaseReact


class CommonController(object):
    def __init__(self, config: dict):
        self.window_title = config["window_title"]
        self.recognizer : BaseRecognizer = config["recognizer"]
        self.react : BaseReact = config["react"]

        self.frame_seconds = 1 / config["fps"]
        self.frame_max_running = config["frame_max_running"]

    def main_loop(self):
        tic = time.time()
        next_tick = tic + self.frame_seconds

        crt_frame = 0

        while crt_frame < self.frame_max_running:
            crt_frame += 1
            if (toc := time.time()) < next_tick:
                time.sleep((next_tick - toc) * random.random())
            next_tick = time.time() + self.frame_seconds
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
            try:
                # perceive
                coords, screenshot = capture_window(self.window_title)
            except Exception as e:
                print(f"捕获窗口失败: {e}")
                continue

            # recognize
            maybe_result = self.recognizer.recognize(screenshot)

            # react
            gui_action = self.react.react(maybe_result)

            # execute
            gui_action.execute(coords)
        
        print("Main Loop End")