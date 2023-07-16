# How to run
- Install the requirements  
```pip install requirements.txt```  
- Run the app
```cd exercise_tracker```
```python manage.py runserver```
- To see the API documentation and test it with Swagger go to ```http://localhost:8000/swagger```
- To run unit tests ```python manage.py test app.tests```

## Migrations
- To make the migrations (when changes are made to the db models):
```python manage.py makemigrations app``` 
- To apply the migrations to the db:
```python manage.py migrate```