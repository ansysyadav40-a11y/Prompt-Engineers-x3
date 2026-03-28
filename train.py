from ultralytics import YOLO

# Load base model
model = YOLO("yolov8n.pt")

# Train model
model.train(
    data="backend/dataset.yaml",
    epochs=10,
    imgsz=256,
    batch=8,
    name="smart_bin_model"
)

print("Training Completed")