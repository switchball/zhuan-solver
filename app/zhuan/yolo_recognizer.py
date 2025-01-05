import numpy as np
from PIL import Image

from ultralytics import YOLO
from controller.perceive.split_utils import split_image


class YOLORecognizer:
    """借助YOLO模型识别棋盘的各个格子"""
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def recognize(self, full_image: Image):
        rows = 14
        cols = 10
        img_list = split_image(full_image, rows=rows, cols=cols)
        results = self.model.predict(source=img_list)
        top_category = [result.probs.top1 for result in results]
        recognize_result = np.array(top_category).reshape(rows, cols)
        return recognize_result
