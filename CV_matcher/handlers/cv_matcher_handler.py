import numpy as np
from transformers import AutoTokenizer
import tritonclient.http as httpclient

tokenizer = AutoTokenizer.from_pretrained(
    "/app/handlers/weights/rubert_onnx/",
    # export=True,
    provider="CUDAExecutionProvider",
)

client = httpclient.InferenceServerClient(url="127.0.0.1:8000")


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


def embed_bert_cls(text):
    t = tokenizer(text, padding=True, truncation=True, return_tensors="np")
    input = []
    for i in t:
        input_temp = httpclient.InferInput(i, t[i].shape, datatype="INT64")
        input_temp.set_data_from_numpy(t[i], binary_data=True)
        input.append(input_temp)
    outputs = client.infer(model_name="feature_extractor", inputs=input)
    out_np = outputs.as_numpy('last_hidden_state')[0, 0, :]
    embedding = normalize(out_np)
    return embedding.tolist()


def get_text_vector(file_full_path):
    with open(file_full_path, "r") as f:
        text = f.read()
    embedding = embed_bert_cls(text)
    return embedding
