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


from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

import config


client 		= TwilioRestClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
NUMBER 		= config.TWILIO_NUMBER
DOMAIN_NAME = config.DOMAIN_NAME



def send_SMS(to, body):
	""" 
	@param {int | str} to
	@param {str} body

	Sends SMS message to 'to' number with message 'body'
	"""
	try:
		client.messages.create(to=to, from_=NUMBER, body=body)
	except TwilioRestException as e:
		if e.code == 21211:
			raise Exception("{0} is not a valid phonenumber".format(to))
		else:
			raise e


def send_agreement(to, cleaner_name, list_id):
	"""
	@param {int | str} to 		- phonenumber to send message to
	@param {str} cleaner_name 	- cleaner that created agreement 
	@param {str} list_id 		- id of list that will be viewed as agreement 

	Sends message: "[cleaner name] sent you a new cleaning agreement: [link]"
	"""
	message = ("{0} sent you a new cleaning agreement: {1}/list/{2}/agreement".format(cleaner_name, DOMAIN_NAME, list_id))
	send_SMS(to, message)


def send_receipt(to, cleaner_name, receipt_id):
	"""
	@param {int | str} to 		- phonenumber to send message to
	@param {str} cleaner_name 	- cleaner that created agreement 
	@param {str} receipt_id 	- id of receipt for which to send link

	Sends message: "[cleaner name] has finished cleaning your place! [link]"
	"""
	message = ("{0} has finished cleaning your place! {1}/receipt/{2}".format(cleaner_name, DOMAIN_NAME, receipt_id))
	send_SMS(to, message)






