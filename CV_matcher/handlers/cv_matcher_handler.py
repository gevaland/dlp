import sys
from transformers import AutoTokenizer

sys.path.append("../infrastructure/")

from inference_model import TritonInference

tokenizer = AutoTokenizer.from_pretrained(
    "/app/handlers/weights/rubert_onnx/",
    # export=True,
    provider="CUDAExecutionProvider",
)

triton = TritonInference()


def get_text_vector(file_full_path):
    with open(file_full_path, "r") as f:
        text = f.read()
    embedding = triton.CV_matcher.embed_bert_cls(text)
    return embedding
