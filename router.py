"""Post-project reconstruction of the reported image-level routing policy."""
from dataclasses import dataclass
import math

WEIGHTS = {'person': .60, 'two_wheeler': .56, 'car': .76,
           'large_vehicle': .51, 'tricycle': .43}

@dataclass(frozen=True)
class Decision:
    use_large: bool
    score: float | None
    reason: str


def route(detections, threshold=.4):
    """Accept (class_name, confidence) pairs in the final five-class label space.

    Invalid labels/scores raise rather than silently bypassing the fallback.
    This score is a reliability heuristic, not a calibrated probability.
    """
    if isinstance(threshold, bool) or not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError('threshold must be finite and in [0, 1]')
    scores = []
    for label, confidence in detections:
        if label not in WEIGHTS:
            raise ValueError('expected a canonical five-class label')
        if isinstance(confidence, bool) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError('confidence must be finite and in [0, 1]')
        scores.append(confidence * WEIGHTS[label])
    if not scores:
        return Decision(True, None, 'empty_detections')
    score = math.fsum(scores) / len(scores)
    return Decision(score < threshold, score, 'below_threshold' if score < threshold else 'accepted')
