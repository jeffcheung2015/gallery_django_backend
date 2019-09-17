Hosted: AWS elastic beanstalk <br/>
Database: AWS RDS <br/>
Elastic search: AWS Elastic service <br/>
Data storage: AWS S3 <br/>
Version control: AWS CodeCommit <br/>
http://django-dev.ap-southeast-1.elasticbeanstalk.com/<br/>
<br/>
<br/>
clone backend:<br/>
this repository<br/><br/>
clone frontend:<br/>
https://github.com/jeffcheung2015/gallery_react_frontend<br/>

Steps to build both backend and frontend:<br/>
clone both backend and frontend <br/>
to run the server, run `source venv/bin/activiate`<br/>
then go into backend folder<br/>
run `python manage.py migrate` [only 1st time running]<br/>
run `python manage.py shell`<br/>
copy and paste the content of '/backend/backend/prerunScripts' into the shell and run them.<br/>
run `python manage.py runserver`<br/>

then for the frontend part,<br/>
run `yarn install` [only 1st time runnning]<br/>
run `yarn start` to start the frontend server<br/>
<br/>
<br/>
steps to serve the reactjs 's index.html template in just backend side:<br/>
first run `yarn build` in frontend folder<br/>
then move the build folder into the backend folder<br/>
the backend settings.py already has those variables all set and pointing to the corresponding directory [e.g. static / media]<br/>
then only running `python manage.py runserver` is needed<br/>

