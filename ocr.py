"""
ocr.py — Resin Code Detection via OCR + Pattern Matching

Detects the recycling resin codes (1–7) stamped on plastic items using
a multi-stage image preprocessing pipeline for maximum accuracy.

Strategy:
  1. Find high-contrast regions likely to contain stamped codes.
  2. Apply adaptive thresholding + morphological ops to isolate digits.
  3. Run Tesseract in digit-only mode.
  4. Regex-match for the resin triangle pattern or standalone 1–7 digits.
  5. Return the code (int) + a base64 crop of the region for debugging.

Tesseract is optional — if not installed, the function degrades gracefully.
"""

import cv2
import numpy as np
import re
import base64
import logging
from typing import Optional, Tuple

log = logging.getLogger(__name__)

# ── Tesseract setup ─────────────────────────────────────────────────────────
_TESSERACT_AVAILABLE = False
pytesseract = None

try:
    import pytesseract as _pt

    # Common install paths — add yours if different
    import platform, os
    if platform.system() == "Windows":
        candidates = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for path in candidates:
            if os.path.exists(path):
                _pt.pytesseract.tesseract_cmd = path
                break

    # Quick sanity-check
    _pt.get_tesseract_version()
    pytesseract = _pt
    _TESSERACT_AVAILABLE = True
    log.info("Tesseract OCR is available.")
except Exception as e:
    log.warning(f"Tesseract not available ({e}). Resin OCR will be disabled.")


# ── Constants ────────────────────────────────────────────────────────────────
VALID_CODES = set(range(1, 8))   # 1–7
TESSERACT_CONFIG = "--oem 3 --psm 7 -c tessedit_char_whitelist=1234567"


# ── Public API ────────────────────────────────────────────────────────────────
def detect_resin_code(frame: np.ndarray) -> Tuple[Optional[int], Optional[str]]:
    """
    Scan a frame for a plastic resin code (1–7).

    Returns:
        (code, region_b64)
        code       : int 1–7, or None if not found
        region_b64 : base64-encoded JPEG of the detected region (for debug UI)
    """
    if not _TESSERACT_AVAILABLE:
        return None, None

    h, w = frame.shape[:2]

    # ── Stage 1: Search the most likely regions ───────────────────────────
    # Resin codes are usually on the bottom third of the container.
    # We also search the full frame as a fallback.
    regions = _get_search_regions(frame)

    for region_frame, (rx, ry) in regions:
        code = _ocr_region(region_frame)
        if code is not None:
            # Encode the matching region for the frontend
            region_b64 = _encode_region(region_frame)
            log.info(f"Resin code {code} detected at region offset ({rx},{ry})")
            return code, region_b64

    return None, None


# ── Internal Helpers ──────────────────────────────────────────────────────────
def _get_search_regions(frame: np.ndarray) -> list[Tuple[np.ndarray, Tuple[int, int]]]:
    """
    Return candidate sub-regions sorted by likelihood.
    (subframe, (offset_x, offset_y))
    """
    h, w = frame.shape[:2]
    regions = []

    # Bottom third (most common location for resin codes)
    y_start = int(h * 0.6)
    regions.append((frame[y_start:h, :], (0, y_start)))

    # Centre of frame
    cy, cx = h // 2, w // 2
    pad = min(h, w) // 4
    regions.append((frame[cy - pad:cy + pad, cx - pad:cx + pad], (cx - pad, cy - pad)))

    # Full frame (last resort)
    regions.append((frame, (0, 0)))

    return regions


def _ocr_region(region: np.ndarray) -> Optional[int]:
    """
    Apply multi-stage preprocessing then OCR a region.
    Returns a valid code int (1–7) or None.
    """
    preprocessed_variants = _preprocess(region)

    for variant in preprocessed_variants:
        code = _run_ocr(variant)
        if code is not None:
            return code

    return None


def _preprocess(img: np.ndarray) -> list[np.ndarray]:
    """
    Return a list of preprocessed image variants for OCR.
    Multiple variants maximise the chance of a successful read.
    """
    # Resize to give Tesseract larger pixels to work with
    scale = max(1, 400 // max(img.shape[:2]))
    if scale > 1:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img.copy()

    variants = []

    # 1. Plain grayscale
    variants.append(gray)

    # 2. CLAHE (contrast-limited adaptive histogram equalisation) — great for embossed codes
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    variants.append(clahe.apply(gray))

    # 3. Otsu global threshold
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variants.append(otsu)

    # 4. Adaptive threshold (good for uneven lighting)
    adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )
    variants.append(adaptive)

    # 5. Inverted adaptive (dark-on-light codes)
    variants.append(cv2.bitwise_not(adaptive))

    # 6. Morphological opening on Otsu (removes noise, keeps digits)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morphed = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, kernel)
    variants.append(morphed)

    return variants


def _run_ocr(img: np.ndarray) -> Optional[int]:
    """
    Run Tesseract on a single preprocessed image.
    Returns a valid code int (1–7) or None.
    """
    try:
        text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG).strip()
    except Exception as e:
        log.debug(f"Tesseract error: {e}")
        return None

    return _extract_code(text)


def _extract_code(text: str) -> Optional[int]:
    """
    Parse OCR output to find a resin code.

    Looks for:
      - The recycling triangle pattern: a digit inside ♻ / △ / [N]
      - A standalone digit 1–7 appearing on its own
      - Any digit 1–7 adjacent to common resin markers
    """
    if not text:
        return None

    # Strip whitespace and normalise
    text = text.strip().replace("\n", " ").replace("\x0c", "")

    # Pattern 1: digit inside triangle-like markers (OCR often reads the triangle as chars)
    triangle_pattern = re.search(r'[△▲\[\(]?\s*([1-7])\s*[▽▼\]\)]?', text)
    if triangle_pattern:
        candidate = int(triangle_pattern.group(1))
        if candidate in VALID_CODES:
            return candidate

    # Pattern 2: lone single-digit on a line
    for line in text.split():
        line = line.strip()
        if line in {str(i) for i in VALID_CODES}:
            return int(line)

    # Pattern 3: digit anywhere in short strings (< 5 chars)
    if len(text) <= 5:
        match = re.search(r'([1-7])', text)
        if match:
            return int(match.group(1))

    return None


def _encode_region(img: np.ndarray) -> str:
    """Encode a cv2 image as a base64 JPEG string."""
    try:
        _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return base64.b64encode(buf).decode("utf-8")
    except Exception:
        return ""