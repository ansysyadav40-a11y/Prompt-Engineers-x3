"""
EcoLens — AI Smart Bin Backend
Flask API powering real-time waste detection, OCR resin code reading,
disposal instructions, and carbon impact tracking.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import time
import logging

from detector import detect_objects
from instructions import get_disposal_info, WASTE_CATEGORIES
from ocr import detect_resin_code

# ──────────────────────────────────────────────
# App Setup
# ──────────────────────────────────────────────
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def decode_image(file_storage=None, b64_string=None) -> np.ndarray:
    """Accept either a file upload or a base64-encoded string."""
    if file_storage:
        img_bytes = file_storage.read()
    elif b64_string:
        # Strip data-URL prefix if present
        if "," in b64_string:
            b64_string = b64_string.split(",", 1)[1]
        img_bytes = base64.b64decode(b64_string)
    else:
        raise ValueError("No image data provided.")

    arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Failed to decode image — unsupported format.")
    return frame


def encode_image(frame: np.ndarray) -> str:
    """Encode a cv2 frame to base64 JPEG string."""
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf).decode("utf-8")


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "2.0.0", "model": "YOLOv8n"})


@app.route("/api/detect", methods=["POST"])
def detect():
    """
    POST /api/detect
    Body: multipart/form-data  → field: 'image' (file)
       OR application/json    → field: 'image_b64' (base64 string)

    Returns JSON with detections, disposal info, resin code, annotated frame.
    """
    t0 = time.time()

    try:
        # 1. Decode incoming image
        if request.content_type and "multipart" in request.content_type:
            if "image" not in request.files:
                return jsonify({"error": "No image field in form data."}), 400
            frame = decode_image(file_storage=request.files["image"])
        else:
            data = request.get_json(silent=True) or {}
            if "image_b64" not in data:
                return jsonify({"error": "Provide 'image_b64' in JSON body or 'image' as form-data."}), 400
            frame = decode_image(b64_string=data["image_b64"])

        original_h, original_w = frame.shape[:2]
        log.info(f"Frame received: {original_w}×{original_h}")

        # 2. Object detection
        detections = detect_objects(frame)

        # 3. Resin code OCR (runs on full frame for best coverage)
        resin_code, resin_region_b64 = detect_resin_code(frame)
        resin_info = get_resin_info(resin_code)

        # 4. Enrich detections with disposal info
        enriched = []
        for det in detections:
            info = get_disposal_info(det[0]["label"])
            enriched.append({
                **det,
                "disposal": info,
            })

        # 5. Draw annotated frame
        annotated = draw_detections(frame.copy(), enriched, resin_code)
        annotated_b64 = encode_image(annotated)

        # 6. Top result summary (highest confidence detection)
        top = enriched[0] if enriched else None

        elapsed_ms = round((time.time() - t0) * 1000, 1)
        log.info(f"Detected {len(enriched)} object(s) in {elapsed_ms}ms. Top: {top['label'] if top else 'none'}")

        return jsonify({
            "success": True,
            "elapsed_ms": elapsed_ms,
            "detection_count": len(enriched),
            "detections": enriched,
            "top": top,
            "resin": {
                "code": resin_code,
                "info": resin_info,
                "region_b64": resin_region_b64,
            },
            "annotated_frame_b64": annotated_b64,
        })

    except ValueError as e:
        log.warning(f"Client error: {e}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        log.exception("Unexpected error during detection")
        return jsonify({"success": False, "error": "Internal server error. See server logs."}), 500


@app.route("/api/categories", methods=["GET"])
def categories():
    """Return all supported waste categories and their metadata."""
    return jsonify({"categories": WASTE_CATEGORIES})


# ──────────────────────────────────────────────
# Resin Code Info
# ──────────────────────────────────────────────
RESIN_MAP = {
    1: {"code": 1, "name": "PET",  "full": "Polyethylene Terephthalate",  "recyclable": True,  "note": "Widely accepted — water/soda bottles, food trays."},
    2: {"code": 2, "name": "HDPE", "full": "High-Density Polyethylene",   "recyclable": True,  "note": "Widely accepted — milk jugs, shampoo bottles, detergent."},
    3: {"code": 3, "name": "PVC",  "full": "Polyvinyl Chloride",          "recyclable": False, "note": "Rarely recyclable — pipes, window frames. Do NOT burn."},
    4: {"code": 4, "name": "LDPE", "full": "Low-Density Polyethylene",    "recyclable": True,  "note": "Plastic bags, squeezable bottles — check local drop-off."},
    5: {"code": 5, "name": "PP",   "full": "Polypropylene",               "recyclable": True,  "note": "Yogurt containers, bottle caps, straws."},
    6: {"code": 6, "name": "PS",   "full": "Polystyrene",                 "recyclable": False, "note": "Styrofoam — avoid. Rarely accepted in curbside recycling."},
    7: {"code": 7, "name": "Other","full": "Mixed / Other Plastics",      "recyclable": False, "note": "Check local rules. Often non-recyclable."},
}

def get_resin_info(code):
    if code is None:
        return None
    return RESIN_MAP.get(int(code))


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    log.info("🌿 EcoLens backend starting on http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)