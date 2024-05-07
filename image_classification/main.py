from ultralytics import YOLO

#Load Model
model = YOLO("yolov8n.yaml")
results = model.train(data="config.yaml", epochs=3)