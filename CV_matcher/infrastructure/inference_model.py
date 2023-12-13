import tritonclient.http as httpclient
from model_class import Road_sign_detector


class TritonInference:
    def __init__(self, url="127.0.0.1:8000"):
        self.client = httpclient.InferenceServerClient(url=url)
        self.road_sign_detector = Road_sign_detector(self.client)
