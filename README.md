## Инструкции:

#	1. Выполнить в корневой папке проекта:
```
		Для Unix систем: 		source venv/bin/activate 
		Для Windows:				.\venv\Scripts\activate
```	
#	2. Выполнить в корневой папке проекта:
```
			flask run 
```	
## Использование 		
* Поле id - обязательное для всех PUT и DELETE запросов
* Поле name - обязательное для всех POST запросов. 
* Поле project_id - обязательное для POST запросов на endpoint /tasks