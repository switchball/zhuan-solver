from ultralytics import YOLO, checks, hub


def train_yolo(model_path, data_path, epochs=100):
    if model_path is None:
        model_path = "yolov8n-cls.pt"
    model = YOLO(model_path)
    model.train(mode="classify", data=data_path, epochs=epochs, imgsz=128)


if __name__ == '__main__':
    train_yolo(
        model_path='runs/classify/train/weights/best.pt',
        data_path="zhuan_v1",  # in datasets/...
        epochs=50
    )