# Google's OAuth2 implementation with Flask
In this project I implemented Google OAuth2 authentication using Flask. To work, the app needs the ```client_secret.json``` file
that it is a file that contains the Oauth2 credentials and you can get it through the Google API Console service.
## How it works
Once you have the client_secret.json file, make sure the file path is configured correctly in the CLIENT_SECRET_JSON_PATH variable in the config.py module, then:
- install the requirements  
```pip install requirements.txt```
- run the app  
```python app.py```
- once you start the app you can go to the ```/auth/login``` route to authenticate
- once authenticated, you will be redirected to route ```/protected-area``` which will display message "Welcome to the protected area, <your_name> <your_surname>" and a button to log out.