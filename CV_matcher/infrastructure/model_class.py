import cv2
import numpy as np
import tritonclient.http as httpclient
from transformers import AutoTokenizer


class CV_matcher:
    def __init__(self, client):
        self.client = client
        self.tokenizer = AutoTokenizer.from_pretrained(
            "/app/handlers/weights/rubert_onnx/",
            # export=True,
            provider="CUDAExecutionProvider",
        )

    def normalize(self, v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    def embed_bert_cls(self, text):
        t = self.tokenizer(
            text, padding=True, truncation=True, return_tensors="np"
        )
        input = []
        for i in t:
            input_temp = httpclient.InferInput(i, t[i].shape, datatype="INT64")
            input_temp.set_data_from_numpy(t[i], binary_data=True)
            input.append(input_temp)
        outputs = self.client.infer(
            model_name="feature_extractor", inputs=input
        )
        out_np = outputs.as_numpy("last_hidden_state")[0, 0, :]
        embedding = self.normalize(out_np)
        return embedding.tolist()
