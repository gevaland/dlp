# Deep Learning in Practice

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
    System_Ext(tritonApi, "Triton Inference Server", "Запускает модель <br> на инференс")

    Container_Boundary(appContainer, "Streamlit", "Приложение для запроса данных по разметке") {
        Component(streamlitComponent, "Инференс", "Python", "Загрузка и обработка <br> видео, содержащего <br> дорожные знаки")
        Component(statComponent, "Статистика", "Python", "Статистика <br> работы сервиса")
    }

    Rel(personUser, nginxApi,,)
    Rel(nginxApi, streamlitComponent,,)
    Rel(nginxApi, statComponent,,)
    Rel(streamlitComponent, postgresqlDb,,)
    Rel(streamlitComponent, tritonApi,,)
```
