# CV Matcher

## Требования к продукту

Рассмотрим требования на диаграме SysML REQ
```mermaid
    requirementDiagram

    requirement req1 {
    id: 1
    text: "Разработать систему
            рекомендаций CV"
    risk: medium
    verifymethod: test
    }

    designConstraint req2 {
    id: 2
    text: "HTTP JSON-RPC
            сервис с загрузкой
            CV файлов"
    risk: low
    verifymethod: analysis
    }

    functionalRequirement req11 {
    id: 1.1
    text: "Рекомендовать
            подходящие описания
            по запросу CV"
    risk: low
    verifymethod: inspection
    }

    functionalRequirement req12 {
    id: 1.1
    text: "Находить общие
            топики по запросу CV"
    risk: low
    verifymethod: inspection
    }

    performanceRequirement req13 {
    id: 1.2
    text: "Отвечать по HTTP
            за 5s"
    risk: medium
    verifymethod: inspection
    }

    interfaceRequirement req121 {
    id: 1.2.1
    text: "HTTP JSON-RPC
            рекомендательный сервис"
    risk: medium
    verifymethod: demonstration
    }

    physicalRequirement req122 {
    id: 1.2.2
    text: "Физ.машина
        2cpu, 8Gmem"
    risk: medium
    verifymethod: analysis
    }

    req1 - traces -> req11
    req2 - derives -> req1
    req11 - contains -> req13
    req11 - contains -> req12
    req13 - contains -> req121
    req121 - derives -> req122
    req122 - refines -> req13
```


## Системный дизайн

Рассмотрим системный дизайн на архитектурных диаграммах C4 Model:
```mermaid
C4Context
    accTitle: CV Matcher
    accDescr: Components

    Person(personUser, "Юзер", "Пользователь, который <br> использует приложение")

    System(nginxApi, "API Gateway", "Проксирует вызовы <br> с фасада во <br> внутренние системы")
    SystemDb(postgresqlDb, "PostgreSQL DB", "БД всех CV и <br> вектора")
    System(recsys, "RecSys Service", "Запускает модель <br> на инференс")
    System_Ext(tritonSystemE, "Triton Inference Server", "Запускает модель <br> на инференс")

    Container_Boundary(recsysContainer, "RecSys", "Приложение для рекомендаций CV") {
        Component(statComponent, "Статистика", "Python", "Статистика <br> работы сервиса")
        Component(recsysComponent, "Инференс", "Python", "Загрузка и обработка <br> CV")
    }

    Container_Boundary(fastapiContainer, "Fastapi", "Приложение для взаимодействия между сервисами") {
        Component(fastapiComponent, "Медиатор", "Python", "Взаимодействие <br> с рекомендациями")
    }

    Rel(personUser, nginxApi,,)
    Rel(nginxApi, recsysComponent,,)
    Rel(nginxApi, statComponent,,)
    Rel(recsysComponent, fastapiComponent,,)
    Rel(fastapiComponent, postgresqlDb,,)
    Rel(fastapiComponent, recsys,,)
    Rel(fastapiComponent, tritonSystemE,,)
```

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
