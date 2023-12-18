## Использование
Чтобы запустить наш сервис необходимо использовать команды:
```sh
git clone [https://github.com/BekusovMikhail/number_plate.git](https://github.com/gevaland/dlp.git)
cd dlp/CV_matcher
docker compose build
docker compose up --wait

http://127.0.0.1:8501/
```
**Если у вас появляются подобные предупреждения**  
![image](https://github.com/gevaland/dlp/assets/63633043/a3b80e96-885a-4d8a-80df-4c344d65e13b)  
**Запустите команду ``docker compose up --wait`` еще раз**

Нужно скачать папку [triton_model_repo](https://drive.google.com/drive/folders/1zUPhzSTosEZQAJinMLVhcKhjrkHA7FRB?usp=sharing) и перенести ее в **...dlp/CV_matcher/**
## Документация
Документация доступна по url  
```http://127.0.0.1:8600/docs```
