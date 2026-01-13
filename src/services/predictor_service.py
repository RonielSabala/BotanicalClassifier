import os

from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from dotenv import load_dotenv
from msrest.authentication import ApiKeyCredentials

load_dotenv()
key = os.getenv("KEY")
endpoint = os.getenv("ENDPOINT")
project_id = os.getenv("PROJECT_ID")
published_name = os.getenv("PUBLISHED_ITERATION_NAME")

credentials = ApiKeyCredentials(in_headers={"Prediction-key": key})  # type: ignore
client = CustomVisionPredictionClient(endpoint, credentials)


def get_flower_prediction(flower_image_path: str) -> list[tuple[str, float]]:
    """
    Devuelve la predicción del modelo a una imagen.
    """

    with open(flower_image_path, "rb") as image:
        results = client.classify_image(project_id, published_name, image.read())
        return [
            (prediction.tag_name, prediction.probability)
            for prediction in results.predictions  # type: ignore
        ]
