import time
import logging
from ultralytics import YOLO

model = None


def load_model():
    global model
    if model is None:
        logging.info("Loading YOLOv8n model…")
        model = YOLO("yolov8n.pt")
        logging.info("Model loaded.")
    return model


def smart_label(label):

    mapping = {
        "bottle": "Plastic Bottle",
        "cup": "Plastic Cup",
        "wine glass": "Glass Bottle",
        "book": "Paper",
        "cell phone": "E-Waste",
        "laptop": "E-Waste",
        "keyboard": "E-Waste",
        "mouse": "E-Waste",
        "remote": "Plastic Waste",
        "toothbrush": "Plastic Waste",
        "tv": "E-Waste"
    }

    return mapping.get(label, "General Waste")


def get_category(label):

    plastic = ["bottle", "cup", "remote", "toothbrush"]
    paper = ["book"]
    ewaste = ["cell phone", "laptop", "keyboard", "mouse"]

    if label in plastic:
        return "Plastic Waste"

    elif label in paper:
        return "Paper Waste"

    elif label in ewaste:
        return "E-Waste"

    else:
        return "General Waste"


def get_disposal(category):

    rules = {

        "Plastic Waste": {
            "bin": "🟦 Blue Bin",
            "instruction": "Clean and recycle plastic"
        },

        "Paper Waste": {
            "bin": "🟩 Green Bin",
            "instruction": "Keep dry before recycling"
        },

        "E-Waste": {
            "bin": "🟥 E-Waste Bin",
            "instruction": "Dispose at e-waste center"
        },

        "General Waste": {
            "bin": "⬛ General Bin",
            "instruction": "Dispose normally"
        }

    }

    return rules.get(category)


def detect_objects(image):

    model = load_model()

    start = time.time()

    results = model(image)[0]

    detections = []

    for box in results.boxes:

        label = model.names[int(box.cls)]
        confidence = float(box.conf)

        if confidence < 0.35:
            continue

        smart = smart_label(label)
        category = get_category(label)
        disposal = get_disposal(category)

        detections.append({
            "label": smart,
            "confidence": confidence,
            "category": category,
            "disposal": disposal
        })

    detections.sort(key=lambda x: x["confidence"], reverse=True)

    top = detections[0] if detections else None

    elapsed = (time.time() - start) * 1000

    logging.info(
        f"Detected {len(detections)} object(s) in {elapsed:.1f}ms. "
        f"Top: {top['label'] if top else 'none'}"
    )

    return detections, top