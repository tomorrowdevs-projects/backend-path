# How to run
- Install the requirements  
```pip install requirements.txt```  
- Run the app
```cd exercise_tracker```
```python manage.py runserver```

## Migrations
- To make the migrations (when changes are made to the db models):
```python manage.py makemigrations app``` 
- To apply the migrations to the db:
```python manage.py migrate```