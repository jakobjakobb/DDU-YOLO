from ultralytics import YOLO
import os

DIR = os.path.dirname(os.path.abspath(__file__))

MODEL = "yolo26n.pt"
DATA = os.path.join(DIR, "dataset", "data.yaml")
EPOCHS = 30
IMGSZ = 640
PATIENCE = 10

if __name__ == "__main__":
    model = YOLO(os.path.join(DIR, MODEL))

    model.train(
        data=DATA,
        epochs=EPOCHS,
        imgsz=IMGSZ,
        patience=PATIENCE,
        project=os.path.join(DIR, "runs"),
        name="train",
    )