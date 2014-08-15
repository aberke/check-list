
<img width="200px" src="http://www.neat-streak.com/static/icon/neatstreak-logo-200px.png" alt="logo" align="right" />

check-list
==========

Significance Labs project prototype - Checklists for house cleaners

<http://neat-streak.com>

[Watch our 1 minute demo video](http://www.neat-streak.com/info/)


Running Locally
---

* Clone/fork repo 

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
* Set necessary environment variables (see **Environment Variables** section below)
* Run server ```$ python main.py``` and visit <http://127.0.0.1:3000>


Running The Tests
---

* Ensure environment variables are set and in virtualenv
* From the base directory ```$ python run_tests.py```


Environment Variables
---

The following environment variables must be set in order for the project to run.
* TWILIO_ACCOUNT_SID
* TWILIO_AUTH_TOKEN
* DOMAIN_NAME
* BASIC_AUTH_USERNAME
* BASIC_AUTH_PASSWORD

You can either obtain the ```env.sh``` file from Alex (aberke) OR create your own:

1. Create a [Twilio](https://www.twilio.com/) account and load it up with a dollar or two
  * We need to send a few SMS messsages and each costs a fraction of a cent
  * From your account, obtain your TWILIO ACCOUNT SID and TWILIO AUTH TOKEN
2. Put the following in ```env.sh```
```
export TWILIO_ACCOUNT_SID="YOUR TWILIO ACCOUNT SID"
export TWILIO_AUTH_TOKEN="YOUR TWILIO ACCOUNT TOKEN"

export DOMAIN_NAME="http://127.0.0.1:3000"

export BASIC_AUTH_USERNAME=""
export BASIC_AUTH_PASSWORD=""
```

Make sure ```env.sh``` is in the base directory and run ```$ source env.sh```


Admin and Analytics
---

There's an admin tool to view all the active users
* Navigate to [/backstage/](http://www.neat-streak.com/backstage/)
* Protected with HTTP Basic Auth
  * Credentials set in env.sh ```BASIC_AUTH_USERNAME``` and ```BASIC_AUTH_PASSWORD```
  * Play with it when running locally or get credentials for www.neat-streak.com from Alex (aberke)

Ask Alex (aberke) for access to our [Google Analytics](https://www.google.com/analytics/web/?authuser=2#report/visitors-overview/a52152670w85170631p88292434/)


Work Flow
---

Branches: 
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
- Can easily toggle between languages in the UI
- Device/browser language detected  and used as default language

***Implemention via Google Spreadsheet + AngularJS + language package***

- Google doc spreadsheet contains the terms we need translated
	- JSON pulled from this document at each server restart
	- <https://docs.google.com/a/significancelabs.org/spreadsheets/d/1O2VvGGMeIEeugPa-TBBk7sKt4Kstdw31bphQ5jDp71c/edit#gid=0>

- Separate AngularJS ***translateModule*** handles all client-side translations
	- translate filter used in HTML to handle all copy
		- filter syntax: ```{{ 'KEYNAME' | translate: 'format' }}```
			- ```'KEYNAME'``` is the keyname (column A of spreadsheet) that maps to the translations
			- ```'format'``` is the format in which to present the translation, eg: ```'uppercase'``` or ```'titlecase'```
		- example use: ```{{ 'SAVE' | translate: 'uppercase' }}```
	- TranslateService does the actual work of translations
		- utilized by filter and controllers
		- interfaces with the language blueprint

- language package is a Flask blueprint
	- User's last language is stored in session
	- Constructs map of translations from Google Doc spreadsheet


Domain Name Configuration
---

- Production server (URL for users): <http://www.neat-streak.com>
- Staging server: <http://staging.neat-streak.com>

- The following redirect to <http://www.neat-streak.com>
	- <http://neat-streak.com>
	- <http://neat-streak.org>
	- <http://www.neat-streak.org>

Domain names bought from and configured via namecheap.com under Ciara's account


Database
---

* All data stored in mongodb
* Clear out the database with the methods defined in ```/app/database.py```


Authors
---
[This project came out of Significance Labs.](http://significancelabs.org/)

**Hacker:** Alexandra Berke (aberke)
**Designer:** Gaia Orain
**Fellow:** Ciara Byrne



Develop
---

Please contribute via pull requests OR

Get access from one of the authors to the [document with all the info](https://docs.google.com/a/significancelabs.org/document/d/1cTDj2I45l5fA3-1YsgciUx5xUHsXfN75iQRGc4TlzSI/edit)


TODO
---

- test coverage for populate_cleaner in GET /list/<id>
- test coverage for translate method in /language/__init__.py

- organize CSS

- parse URL for mongoHQ in config file

- handle default room data

- handle default list data via google spreadsheets

- protect API endpoints
	- write middleware

- limit Google API key to only my IPs?

- store session in database?
	- if scale number of servers

	










