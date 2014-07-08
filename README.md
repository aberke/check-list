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

- set cache TTL to 0 for /auth/user ?

	










