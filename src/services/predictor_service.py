"""
Service to obtain predictions from Azure Custom Vision and
attach them to Record objects.
"""

from typing import Optional

from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from msrest.authentication import ApiKeyCredentials

from common.settings import settings
from models.prediction_model import TagPrediction
from models.record_model import Record

_CLIENT: Optional[CustomVisionPredictionClient] = None


def _get_client() -> CustomVisionPredictionClient:
    """
    Lazily create and return a `CustomVisionPredictionClient`.
    """

    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    credentials = ApiKeyCredentials(
        in_headers={"Prediction-key": settings.custom_vision_key}
    )

    _CLIENT = CustomVisionPredictionClient(settings.custom_vision_endpoint, credentials)
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
                settings.custom_vision_project_id,
                settings.custom_vision_published_name,
                image.read(),
            )

        record.predictions = [
            TagPrediction(tag_name=str(p.tag_name), probability=float(p.probability))
            for p in results.predictions  # type: ignore
        ]
