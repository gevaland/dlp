import tritonclient.http as httpclient
from model_class import CV_matcher


class TritonInference:
    def __init__(self, url="127.0.0.1:8000"):
        self.client = httpclient.InferenceServerClient(url=url)
        self.CV_matcher = CV_matcher(self.client)
