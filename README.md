## Инструкции:

#	1. Выполнить в корневой папке проекта:
```
	Для Unix систем:	source venv/bin/activate
```	
#	2. Выполнить в корневой папке проекта:
```
	python rest_api.py 
```
#	3. Для запуска тестов:
```
	cd app_restappi
	python tests.py

```	
## Использование 		
* Поле id - обязательное для всех PUT и DELETE запросов
* Поле name - обязательное для всех POST запросов. 
* Поле project_id - обязательное для POST запросов на endpoint /tasks
