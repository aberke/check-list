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


HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', 3000)
DEBUG= True if ENVIRONMENT == 'DEVELOPMENT' else True




# - DOMAIN_NAME ----------------------------------

# domain name depends on environment
# default assumes we're in development 	-> host + port
# staging server 						-> staging.neat-streak.com
# production server 					-> www.neat-streak.com

DOMAIN_NAME = ('http://' + HOST + ':' + str(PORT))
if ENVIRONMENT == 'STAGING':
	DOMAIN_NAME = 'http://staging.neat-streak.com'
elif ENVIRONMENT == 'PRODUCTION':
	DOMAIN_NAME = 'http://www.neat-streak.com'

# ---------------------------------- DOMAIN_NAME -


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


TWILIO_ACCOUNT_SID			= "ACfe08bc02cc35943bf5d332a86e3526a8"
TWILIO_AUTH_TOKEN			= "21e0167335a7f876653f2eb46e98af0c"
TWILIO_NUMBER 				= os.getenv('TWILIO_NUMBER', '+16466473454')

GOOGLE_API_KEY 				= "AIzaSyCJxQK1oDn4U3kbDIK-epf96ckze7fuSHQ"

# language module:
SUPPORTED_LANGUAGES 		= ['en', 'es']
DEFAULT_LANGUAGE 			= 'en'
GOOGLE_API_TRANSLATE_SPREADSHEET_KEY = '1O2VvGGMeIEeugPa-TBBk7sKt4Kstdw31bphQ5jDp71c'



del os