## Использование
Чтобы запустить наш сервис необходимо использовать команды:
```sh
git clone [https://github.com/BekusovMikhail/number_plate.git](https://github.com/gevaland/dlp.git)
cd dlp/CV_matcher
docker compose build
docker compose up
http://127.0.0.1:8501/
```
https://drive.google.com/drive/folders/1uRjhYgJrJFe5PR-Bww4Md0Li7XiSg3ta
Скачать model.onnx [тут]([url](https://drive.google.com/drive/folders/1tpZFDbY_MwyK4KAgyhxSEwcpzqSZjrqn?usp=sharing)) и перенести ее в **...dlp/CV_matcher/handlers/weights/rubert_onnx**
## Документация
Документация доступна по url  
```http://127.0.0.1:8600/docs```
