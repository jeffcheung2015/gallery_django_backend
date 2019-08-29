Steps to build both backend and frontend:
clone both backend and frontend
to run the server, run `source venv/bin/activiate`
then go into backend folder
run `python manage.py migrate` [only 1st time running]
run `python manage.py runserver`

then for frontend part,
run `yarn install` [only 1st time runnning]
run `yarn start` to start the frontend server

to serve the reactjs 's index.html template
first run `yarn build` in frontend folder
then move the build folder into the backend folder
the backend settings.py already have those variables all set to point to the necessary directory [e.g. static / media]
then run `python manage.py runserver` only needed

