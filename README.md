check-list
==========

Significance Labs project prototype - Checklists for house cleaners
<http://neat-streak.com>


Running Locally
---

* Clone repo 

```
$ git clone https://github.com/aberke/check-list.git
$ cd check-list
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
* Run server ```$ python main.py``` and visit <http://127.0.0.1:3000>


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
- Push ```staging``` to staging server
	- staging lives at <http://clean-slate-staging.herokuapp.com/>
- Perform QA on staging
- Merge ```staging``` into ```production```
- Push ```production``` branch to production server
	- production lives at <http://clean-slate2.herokuapp.com/>
- Tag commit to ```production``` branch with updated version number

For Simplicity:
* Configure ```.git/config``` file to push to staging with ```$ git push staging``` and push to production with ```$ git push production```

```
# commands:
#————————————
# git push origin [branchName] 
#	-> pushes to github [branchName]
# git push staging	     
#	-> pushes staging branch to staging(remote) (which merges into remote’s master) 
# git push production
#	-> push staging branch to staging(remote) (which merges into remote’s master)

[remote "origin"]
	url = https://github.com/aberke/check-list.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
[remote "production"]
	url = git@heroku.com:clean-slate2.git
	fetch = +refs/heads/*:refs/remotes/heroku/*
	push = production:master
[remote "staging"]
	url = git@heroku.com:clean-slate-staging.git
	fetch = +refs/heads/*:refs/remotes/staging/*
	push = staging:master

```

Language Support
---

See full documentation in /language/README.md

- Support Spanish and English
- All translations handled client side
- Can easily toggle between languages in the UI
- Device/browser language detected 
	- if user uses spanish, defaults to spanish
	- otherwise defaults to english

Implemention via Google Spreadsheet + AngularJS + language module
- Google doc spreadsheet contains the terms we need translated
	- JSON pulled from this document in real time
	- <https://docs.google.com/a/significancelabs.org/spreadsheets/d/1O2VvGGMeIEeugPa-TBBk7sKt4Kstdw31bphQ5jDp71c/edit#gid=0>
- Separate AngularJS module handles all translations
	- See translateModule
	- translate filter used in HTML to handle all copy
		- filter syntax: ```{{ 'KEYNAME' | translate: 'format' }}```
			- ```'KEYNAME'``` is the keyname (column A of spreadsheet) that maps to the translations
			- ```'format'``` is the format in which to present the translation, eg: ```'uppercase'``` or ```'titlecase'```
		- example use: ```{{ 'SAVE' | translate: 'uppercase' }}```
	- TranslateService does the actual work of translations
		- utilized by filter and controllers
- User's last language is stored server-side in session


Domain Name Configuration
---

- Production server (URL for users): <http://www.neat-streak.com>
- Staging server: <http://staging.neat-streak.com>

- The following redirect to <http://www.neat-streak.com>
	- <http://neat-streak.com>
	- <http://neat-streak.org>
	- <http://www.neat-streak.org>

Domain names bought from and configured via namecheap.com under Ciara's account



TODO
---

- Multilingual:
	- supply language to twilio_tools



- test coverage for populate_cleaner in GET /list/<id>

- organize CSS

- move hamburger-control and control to directives?
	- pro: modularity
	- con: extra files to request

- parse URL for mongoHQ in config file

- handle errors with UI feedback in your controllers errorCallback functions

- handle default room data

- handle default list data via google spreadsheets

- host on AWS?

- protect API endpoints
	- write middleware

- limit Google API key to only my IPs?


- set cache TTL to 0 for /auth/user ?

- store session in database?
	- if scale number of servers

	










