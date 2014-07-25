#********************************************************************************
#--------------------------------------------------------------------------------
#
#	Significance Labs
#	Brooklyn, NYC
#
# 	Author: Alexandra Berke (aberke)
# 	Written: Summer 2014
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************





import os

# test.py sets environment to TESTING, heroku has environment as PRODUCTION or STAGING
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'DEVELOPMENT')

DOMAIN_NAME = os.environ.get('DOMAIN_NAME', 'http://127.0.0.1:3000')

HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', 3000)
DEBUG= True if ENVIRONMENT == 'DEVELOPMENT' else True


# - MONGO ----------------------------------
# if development : host is "mongodb://localhost:27017"
# if production or staging: db is set in host URI, host is in "MONGOHQ_URL" env variable found in '$ heroku config' command
# if TESTING: db is testing specific db

MONGODB_HOST 	= "mongodb://localhost:27017"
MONGODB_DB 		= "check-list"

if ENVIRONMENT == 'PRODUCTION':
	MONGODB_HOST=os.environ.get("MONGOHQ_URL", None)
	MONGODB_DB  = 'app27214918'

if ENVIRONMENT == 'STAGING':
	MONGODB_HOST=os.environ.get("MONGOHQ_URL", None)
	MONGODB_DB  = 'app27785251'

elif ENVIRONMENT == 'TESTING':
	MONGODB_DB 	= "check-list-testing"

# ---------------------------------- MONGO -



SECRET_KEY 					= os.getenv('SESSION_SECRET', 'Significance')


BASIC_AUTH_USERNAME			= os.getenv('BASIC_AUTH_USERNAME', '')
BASIC_AUTH_PASSWORD			= os.getenv('BASIC_AUTH_PASSWORD', '')


TWILIO_ACCOUNT_SID			= os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN			= os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER 				= os.getenv('TWILIO_NUMBER', '+16466473454')

GOOGLE_API_KEY 				= "AIzaSyCJxQK1oDn4U3kbDIK-epf96ckze7fuSHQ"

# AWS_ACCESS_KEY_ID			= os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY		= os.environ['AWS_SECRET_ACCESS_KEY']



del os