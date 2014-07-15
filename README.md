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

* Run server ```python run.py``` and visit<http://127.0.0.1:3000>


Running The Tests
---
From the base directory ```python test.py```


Analytics
---

<https://www.google.com/analytics/web/?authuser=2#report/visitors-overview/a52152670w85170631p88292434/>



TODO
---

- handle errors with UI feedback in your controllers errorCallback functions

- add deleting rooms

- all things marked with TODO in test.py etc

- handle default room data

- handle default list data via google spreadsheets

- test coverage for all api endpoints relating to task

- test coverage for cleaner.update_password and cleaner.password_valid

- move hamburger-control and control to directives?
	- pro: modularity
	- con: extra files to request

- protect API endpoints
	- write middleware


- set cache TTL to 0 for /auth/user ?

- store session in database?
	- if scale number of servers

- lazily POST list on /list/new

	










