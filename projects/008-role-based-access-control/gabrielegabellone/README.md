# How to run
- Install the requirements  
```pip install requirements.txt```
- Run the app   
```python app.py```
- To see the API documentation and test it with Swagger go to http://localhost:5000/apidocs
## Database
This app needs two databases, one called ```user_management_system``` which contains tables of roles and users 
and another empty one called ```test_user_management_system``` for running unit tests, you can create them in two ways: 
- create manually the databases with mysql;
- or run the command ```docker-compose up```.  

Then you have to create the tables, then in the project folder run from the command line:
```flask shell```
```from models import db```
```db.create_all()```
```exit()```

Finally, make sure that the database URIs in config.py and config_tests.py are correct.