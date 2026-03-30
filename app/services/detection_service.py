"""
Detection service — encapsulates fall detection logic.

The interface is stable: run_detection() consumes a numpy frame
and returns a DetectionResult with label and confidence.

Currently: stub with random fall/standing classification.
Later: replace with real YOLO/pose-estimation model without changing this interface.
"""
import random
from dataclasses import dataclass
import numpy as np


@dataclass
class DetectionResult:
    """Result from running detection on a frame."""
    label: str
    confidence: float


def run_detection(frame: np.ndarray) -> DetectionResult:
    """
    Run fall detection on a video frame.
    
    Args:
        frame: numpy array (H x W x C) — typically from OpenCV or decoded base64
        
    Returns:
        DetectionResult with label and confidence 0.65–0.99
    """
    # Stub: random choice of fall/standing
    label = random.choice(["fall", "standing"])
    confidence = random.uniform(0.65, 0.99)
    
    return DetectionResult(label=label, confidence=confidence)
