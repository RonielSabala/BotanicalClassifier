"""
Service to obtain predictions from Azure Custom Vision and
attach them to Record objects.
"""

from typing import Optional

from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from msrest.authentication import ApiKeyCredentials

from common.config import (
    CUSTOM_VISION_ENDPOINT,
    CUSTOM_VISION_KEY,
    CUSTOM_VISION_PROJECT_ID,
    CUSTOM_VISION_PUBLISHED_NAME,
)
from models.prediction_model import TagPrediction
from models.record_model import Record

_CLIENT: Optional[CustomVisionPredictionClient] = None


def _get_client() -> CustomVisionPredictionClient:
    """
    Lazily create and return a CustomVisionPredictionClient.
    """

    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    credentials = ApiKeyCredentials(in_headers={"Prediction-key": CUSTOM_VISION_KEY})  # type: ignore[arg-type]
    _CLIENT = CustomVisionPredictionClient(CUSTOM_VISION_ENDPOINT, credentials)
    return _CLIENT


class PredictorService:
    @staticmethod
    def set_flower_prediction(record: Record) -> None:
        """
        Populate `record.predictions` by sending the record image
        to the Custom Vision API. This mutates the given Record
        in-place.
        """

        if record.predictions is not None:
            return

        client = _get_client()
        with open(record.image_path, "rb") as image:
            results = client.classify_image(
                CUSTOM_VISION_PROJECT_ID, CUSTOM_VISION_PUBLISHED_NAME, image.read()
            )

        record.predictions = [
            TagPrediction(str(p.tag_name), float(p.probability))
            for p in results.predictions  # type: ignore
        ]
