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
from models.prediction_model import Prediction

_credentials = ApiKeyCredentials(in_headers={"Prediction-key": CUSTOM_VISION_KEY})  # type: ignore
_client = CustomVisionPredictionClient(CUSTOM_VISION_ENDPOINT, _credentials)


class PredictorService:
    @staticmethod
    def get_flower_prediction(flower_image_path: str) -> list[Prediction]:
        """
        Devuelve la predicción del modelo a una imagen.
        """

        with open(flower_image_path, "rb") as image:
            results = _client.classify_image(
                CUSTOM_VISION_PROJECT_ID, CUSTOM_VISION_PUBLISHED_NAME, image.read()
            )

        return [
            Prediction(str(prediction.tag_name), float(prediction.probability))
            for prediction in results.predictions  # type: ignore
        ]
