"""
Detection service — real model integration (YOLOv8).
Handles:
frame → model → event → alert
"""

from dataclasses import dataclass
import numpy as np
import torch
import os
from ultralytics import YOLO

from app.crud import create_event, create_alert


# ======================
# LOAD MODEL 
# ======================

MODEL_PATH = os.path.join("app", "ml", 'models', "fall_model.pt")

model = YOLO(MODEL_PATH)  # YOLOv8 loader


# ======================
# DATA STRUCTURE
# ======================

@dataclass
class DetectionResult:
    label: str
    confidence: float


# ======================
# CORE AI LOGIC
# ======================

def run_detection(frame: np.ndarray) -> DetectionResult:
    """
    Runs YOLOv8 inference on a frame.
    Assumes your model has classes like: ['fall', 'standing']
    """

    results = model(frame)

    # Default values
    label = "standing"
    confidence = 0.0

    # Parse YOLO output
    if len(results) > 0:
        boxes = results[0].boxes

        if boxes is not None and len(boxes) > 0:
            # Get highest confidence detection
            confs = boxes.conf.cpu().numpy()
            classes = boxes.cls.cpu().numpy()

            max_idx = confs.argmax()

            confidence = float(confs[max_idx])
            class_id = int(classes[max_idx])

            # Get label name from model
            label = model.names[class_id]

    return DetectionResult(label=label, confidence=confidence)


# ======================
# MAIN HANDLER
# ======================

async def handle_detection(frame, session, device_id, household_id):
    """
    Full pipeline:
    frame → AI → event → alert
    """

    # 1. Run model
    result = run_detection(frame)

    event_id = None
    alert_triggered = False

    # 2. Save event (ALWAYS)
    event = await create_event(
        db=session,
        device_id=device_id,
        type=result.label,
        confidence_score=result.confidence,
    )

    event_id = event.id

    # 3. Trigger alert if fall
    if result.label.lower() == "fall":
        await create_alert(
            db=session,
            event_id=event.id,
            household_id=household_id,
        )
        alert_triggered = True

    # 4. Return result
    return {
        "label": result.label,
        "confidence": result.confidence,
        "event_id": event_id,
        "alert_triggered": alert_triggered,
    }