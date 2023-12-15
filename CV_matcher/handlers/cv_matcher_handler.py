import numpy as np
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForFeatureExtraction
import torch

tokenizer = AutoTokenizer.from_pretrained(
    "/app/handlers/weights/rubert_onnx/",
    # export=True,
    provider="CUDAExecutionProvider",
)
model = ORTModelForFeatureExtraction.from_pretrained(
    "/app/handlers/weights/rubert_onnx/",
    # export=True,
    provider="CUDAExecutionProvider",
)


def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy().tolist()


def get_text_vector(file_full_path):
    with open(file_full_path, "r") as f:
        text = f.read()
    embedding = embed_bert_cls(text, model, tokenizer)
    return embedding
