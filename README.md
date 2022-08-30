# TODO_machine_backend
## Resume
This is the API i made and use in the TODO_machine project. This API is build with Django and Django-rest-framework, implements token auth built-in django and deployment in Render
Link: https://todo-machine.onrender.com/api/
Frontend repo: https://github.com/patxxi/TODO-machine-frontend
Frontend deployment: https://crypto-lambda.netlify.app
### Important note
Render free tier for web services put in rest the app if in the last 15 minutes theres no any request. So may the first request to the api could take some time.
Also, for development you may wanna change DATABASE variable in settings. It is development using Postgress db as well as in the deployment server

## Models

 1. User Model --> Model for the register users
 2. Workspace Model --> Workspace model. It work for split TODOs in differents folders
 3. TODO model --> TODO model. It is the TODO or task

## Endpoints

 - User
	 - api/user/create/ ---> Create new user
	 - api/user/me/ ---> Retrieve logued user
	 - api/user/token/ ---> Create and retrieve authentication token
 - Workspace
	 - api/workspace/ ---> Depends on HTTP method. It work for list user workspaces and create new Workspace
	 - api/workspace/<:id> ---> Depends on HTTP method. It works for retrieve a specify workspace, update it and/or delete it
 - TODO
	 - api/todo/ ---> Depends on HTTP method. Works for list user TODOs and create new TODOs
	 - api/todo/<:id>/ ---> Depends on HTTP method. Works for retrieve specify TODO, update it or delete it

## Commands
 - pip3 install -r requirements.txt --> Install all dependencies
 - python3 manage.py makemigrations
 - python3 manage.py migrate
 - python3 manage.py runserver --> Start dev server