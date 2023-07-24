# How to run
## with docker
- If you use Docker you can execute the command: ```docker-compose up```  
It will create two containers, ```flask-app``` which will install the flask app with its dependencies and ```db``` which
will create two databases, ```user_management_system``` that is the principal db used in the app and 
```test_user_management_system``` that is an empty db used for test purposes.
Docker will also take care of the migrations for the creation of the roles and users tables.
## without docker
- Install the requirements  
```pip install requirements.txt```
- Create two db in mysql, one called ```user_management_system``` and another called ```test_user_management_system```,
then make sure that the database URIs in config.py and config_tests.py are correct.
- Perform the migrations for the creation of the roles and users tables in the db:
```flask db init```
```flask db migrate -m "first migration"```
```flask db upgrade"```
- Run the app   
```python app.py```
## API documentation
- To see the API documentation and test it with Swagger go to http://localhost:5000/apidocs
