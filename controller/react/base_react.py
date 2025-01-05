
from controller.recognize.maybe_result import MaybeResult


class BaseReact:
    def __init__(self):
        pass

    def react(self, result: MaybeResult) -> MouseAction:
        print("[警告] 正在使用默认的 BaseReact 应当继承并返回自定义的动作")
        return None