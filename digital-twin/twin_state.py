from copy import deepcopy
from datetime import datetime, timezone
from threading import RLock


class DigitalTwinState:
    """In-memory virtual patient state for the TwinPulse prototype."""

    def __init__(self, patient_id: str):
        if not patient_id or not patient_id.strip():
            raise ValueError("patient_id cannot be empty")

        self.patient_id = patient_id
        self.created_at = self._now()
        self.updated_at = self.created_at
        self.version = 0
        self.clinical_state = {}
        self.physiological_state = {}
        self.prediction = None
        self.history = []
        self._lock = RLock()

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat()

    def update_clinical_state(self, observations: dict):
        with self._lock:
            self.clinical_state.update(deepcopy(observations))
            self._record("clinical_update", observations)

    def update_physiological_state(self, observations: dict):
        with self._lock:
            self.physiological_state.update(deepcopy(observations))
            self._record("physiological_update", observations)

    def update_prediction(self, prediction: dict):
        with self._lock:
            self.prediction = deepcopy(prediction)
            self._record("prediction_update", prediction)

    def _record(self, event_type: str, payload: dict):
        self.version += 1
        self.updated_at = self._now()
        self.history.append({
            "version": self.version,
            "timestamp": self.updated_at,
            "event_type": event_type,
            "payload": deepcopy(payload),
        })

    def snapshot(self):
        with self._lock:
            return {
                "patient_id": self.patient_id,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "version": self.version,
                "clinical_state": deepcopy(self.clinical_state),
                "physiological_state": deepcopy(self.physiological_state),
                "prediction": deepcopy(self.prediction),
                "history": deepcopy(self.history),
            }
