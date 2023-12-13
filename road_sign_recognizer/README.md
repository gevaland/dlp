# Deep Learning in Practice
# Road Sign Recognition

## Требования к продукту

Рассмотрим требования на диаграме SysML REQ
```mermaid
    requirementDiagram

    requirement req1 {
    id: 1
    text: "Разработать систему
            классификации дорожных
            знаков с камер"
    risk: medium
    verifymethod: test
    }

    designConstraint req2 {
    id: 2
    text: "HTTP JSON-RPC
            сервис с загрузкой
            видео по FTP"
    risk: low
    verifymethod: analysis
    }

    functionalRequirement req11 {
    id: 1.1
    text: "Классифицировать
            Traffic light, Stop sign,
            Traffic sign"
    risk: low
    verifymethod: inspection
    }

    performanceRequirement req12 {
    id: 1.2
    text: "Классифицировать
            видео 15FPS"
    risk: medium
    verifymethod: inspection
    }

    interfaceRequirement req121 {
    id: 1.2.1
    text: "HTTP JSON-RPC
            инференс сервис"
    risk: medium
    verifymethod: demonstration
    }

    physicalRequirement req122 {
    id: 1.2.2
    text: "Физ.машина
            4cpu, 32Gmem,
            RTX3090"
    risk: medium
    verifymethod: analysis
    }

    req1 - traces -> req11
    req2 - derives -> req1
    req11 - contains -> req12
    req12 - contains -> req121
    req121 - derives -> req122
    req122 - refines -> req12
```


## Системный дизайн

Рассмотрим системный дизайн на архитектурных диаграммах C4 Model:
```mermaid
C4Context
    accTitle: Road sign recognizer
    accDescr: Components

    Person(personUser, "Юзер", "Пользователь, который <br> использует приложение")

    System(nginxApi, "API Gateway", "Проксирует вызовы <br> с фасада во <br> внутренние системы")
    SystemDb(postgresqlDb, "Streamlit DB", "БД снимков и <br> результатов расчетов")
    System_Ext(tritonSystemE, "Triton Inference Server", "Запускает модель <br> на инференс")

    Container_Boundary(streamlitContainer, "Streamlit", "Приложение для запроса данных по разметке") {
        Component(statComponent, "Статистика", "Python", "Статистика <br> работы сервиса")
        Component(streamlitComponent, "Инференс", "Python", "Загрузка и обработка <br> видео, содержащего <br> дорожные знаки")
    }

    Container_Boundary(fastapiContainer, "Fastapi", "Приложение для медиатора между сервисами") {
        Component(fastapiComponent, "Медиатор", "Python", "Взаимодействие <br> с инференсом")
    }

    Rel(personUser, nginxApi,,)
    Rel(nginxApi, streamlitComponent,,)
    Rel(nginxApi, statComponent,,)
    Rel(streamlitComponent, fastapiComponent,,)
    Rel(fastapiComponent, postgresqlDb,,)
    Rel(fastapiComponent, tritonSystemE,,)
```

## Формулировка в ML терминах

### Метрики

![Метрики](https://github.com/gevaland/dlp/assets/48095159/3790a893-226b-457c-b4c3-d4fa01b678a2)

### Датасеты и классы

* https://www.kaggle.com/datasets/andrewmvd/road-sign-detection
  * 877 картинок в 4 классах Trafic Light, Stop, Speedlimit, Crosswalk
  * разметка в формате class xmin xmax ymin ymax
  * знаки русские

* https://www.kaggle.com/datasets/valentynsichkar/traffic-signs-dataset-in-yolo-format
  * 741 картинок в 4 классах, разметка Class Number, center in x, center in y, Width Height
  * знаки американские

* https://www.kaggle.com/datasets/barzansaeedpour/traffic-sign-detection?select=classes.txt
  * 703 картинки, штук 30 классов, разметка в формате class xmin xmax ymin ymax
 
### Результаты сравнения моделей

![mAP_50](https://github.com/gevaland/dlp/assets/48095159/aa6420a4-b936-440e-91f0-2d17f0782e75)
![mAP](https://github.com/gevaland/dlp/assets/48095159/70fc9b7e-137b-435f-b962-24f1a2c5a24e)



## Использование

Чтобы запустить наш сервис необходимо выполнить в командной строке:
```sh
git clone https://github.com/gevaland/dlp.git
cd dlp/road_sign_recognizer
docker compose build
docker compose up
```

Не забыть скачать директорию `triton_model_repo` [тут](https://drive.google.com/drive/folders/1uRjhYgJrJFe5PR-Bww4Md0Li7XiSg3ta) и перенести ее в `.../dlp/road_sign_recognizer`

Можно использовать сервис по адресу [тут](http://127.0.0.1:8501/)

## Документация

Документация доступна [тут](http://127.0.0.1:8600/docs)

Видео с демонстрацией работы доступно [тут](https://drive.google.com/file/d/1XgUxX31-SLS5zWhKsPzVJcYSZi00_Zcu/view?usp=drive_link)
