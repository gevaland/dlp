FROM nvcr.io/nvidia/pytorch:22.12-py3

EXPOSE 8600

ENV PYTHONDONTWRITEBYTECODE=1
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY ./fast_api/requirements.txt ./
RUN pip3 install -r requirements.txt

RUN python -m pip install optimum[onnxruntime-gpu]
RUN pip install transformers
RUN python -m pip install psycopg2-binary==2.9.9

WORKDIR /app
COPY . /app
COPY ../handlers /app
COPY ../infrastructure /app
COPY ../configs /app

CMD ["uvicorn", "fast_api.main:app", "--port", "8600"]
