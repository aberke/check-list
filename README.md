check-list
==========

Significance Labs project prototype - Checklists for house cleaners


Running Locally
---

* Clone repo 

```
$ git clone https://github.com/aberke/check-list.git
$ cd /check-list
```

* Create a virutual environment so that the following installations do not cause conflicts.  Make sure to reactivate this virtual environment each time you want to run the server locally.  All the following installations will be isolated in this environment.

```
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```

* Install dependencies: ```$ pip install -r requirements.txt``` (may need to run with sudo)
* Make sure you have mongodb installed ```$ brew install mongodb```
* Make sure mongodb is started ```$ mongod```
* Set necessary environment variables, or obtain environment variable file from Alex and run ```$ source env.sh```
* Run server ```$ python main.py``` and visit<http://127.0.0.1:3000>


Running The Tests
---

* Ensure environment variables are set and in virtualenv
* From the base directory ```$ python run_tests.py```


Analytics
---

<https://www.google.com/analytics/web/?authuser=2#report/visitors-overview/a52152670w85170631p88292434/>

Work Flow
---

Branches: 
- ```working``` branch 	- where work gets done
- ```master``` branch  	- where all outstanding working branches get merged in to
- ```staging``` branch 	- Merges in Master branch when ready to push new features to staging server
- ```production``` branch - Merges in staging when and pushed to production server

Flow:
- Merge in working branches to ```master```
- Merge in ```master``` to ```staging```
- Push ```staging``` to staging server ```$ git push staging staging```
	- staging lives at <http://clean-slate-staging.herokuapp.com/>
	- configure your remote in ```.git/config``` like Alex so that you can just hit ```$ git push staging```
- Perform QA on staging
- Merge ```staging``` into ```production```
- Push to production ```$ git push production production```
	- production lives at <http://clean-slate2.herokuapp.com/>
	- configure your remote in ```.git/config``` like Alex so that you can just hit ```$ git push production```


TODO
---

- parse URL for mongoHQ in config file

- handle errors with UI feedback in your controllers errorCallback functions

- handle default room data

- handle default list data via google spreadsheets

- host on AWS?

- move hamburger-control and control to directives?
	- pro: modularity
	- con: extra files to request

- protect API endpoints
	- write middleware

- limit Google API key to only my IPs?


- set cache TTL to 0 for /auth/user ?

- store session in database?
	- if scale number of servers

- lazily POST list on /list/new

	










