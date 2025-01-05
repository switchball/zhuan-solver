from PIL import Image

from controller.recognize.maybe_result import MaybeResult


class BaseRecognizer:
    def __init__(self):
        pass

    def recognize(self, image: Image) -> MaybeResult:
        print("[警告] 正在使用默认的 BaseRecognizer 应当继承并返回自定义的识别结果")
        return MaybeResult(None, 0)
