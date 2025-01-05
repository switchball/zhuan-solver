import math
import numpy as np
import os
import time
from PIL import Image
from ultralytics import YOLO

from app.zhuan.zhuan_constants import BOARD_AREA_POSITION, NUM_BOARD_ROWS, NUM_BOARD_COLS

from controller.perceive.split_utils import split_image, crop_image
from controller.recognize.maybe_result import MaybeResult


class ZhuanRecognizer:
    def __init__(self, model_path):
        self.board_xywhn = BOARD_AREA_POSITION
        self.model_path = model_path
        self.yolo_recognizer = YOLORecognizer(model_path)
    
    def recognize(self, full_image: Image):
        board_image = crop_image(full_image, self.board_xywhn)
        recognize_result = self.yolo_recognizer.recognize(board_image)
        return MaybeResult(*recognize_result)


class YOLORecognizer:
    """借助YOLO模型识别棋盘的各个格子"""
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def recognize(self, full_image: Image):
        rows = NUM_BOARD_ROWS  # 14
        cols = NUM_BOARD_COLS  # 10
        img_list = split_image(full_image, rows=rows, cols=cols)
        results = self.model.predict(source=img_list, save=False)
        top_category = [result.probs.top1 for result in results]
        top_confidence = [result.probs.top1conf for result in results]
        recognize_result = np.array(top_category).reshape(rows, cols)
        prod_confidence = math.prod(top_confidence)

        self._save_low_conf_images(img_list, top_confidence)

        return recognize_result, prod_confidence

    def _save_low_conf_images(self, img_list, top_confidence, conf=0.9, limit=0.05, img_dir="images/low_conf_images"):
        """保存置信度低于阈值的图片
        
        :param: img_list: 待保存的图片列表
        :param: top_confidence: 置信度列表
        :param: conf: 置信度阈值，默认为 0.9
        :param: limit: 保存图片的最大比例阈值，默认为 0.05
        """
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        ts = int(1000 * time.time())
        low_conf_pair = [(i, confidence) for i, confidence in enumerate(top_confidence) if confidence < conf]

        max_limit = int(len(img_list) * limit)
        if len(low_conf_pair) >= max_limit:
            print(f"超过{max_limit}张({limit*100}%)置信度低于阈值的图片，不再保存以免数据干扰")
            return
        for i, confidence in low_conf_pair:
            img_list[i].save(os.path.join(img_dir, f"addon_{ts}_{i}.png"))
