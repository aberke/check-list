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
from util import APIexception
from app import language


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
			raise APIexception(code=7)
		else:
			raise e


def send_welcome(to, cleaner_name):
	"""
	@param {int | str} to 		- phonenumber to send message to
	@param {str} cleaner_name 	- cleaner name

	Sends message: "Hi [cleaner name]\nWelcome to NeatStreak! [Link to NeatStreak]"
	"""
	message = language.translate("SEND_WELCOME_MESSAGE_SMS")
	message += "\n{1}"
	message = message.format(cleaner_name, DOMAIN_NAME)
	send_SMS(to, message)


def send_agreement(to, cleaner_name, list_id):
	"""
	@param {int | str} to 		- phonenumber to send message to
	@param {str} cleaner_name 	- cleaner that created agreement 
	@param {str} list_id 		- id of list that will be viewed as agreement 

	Sends message: "[cleaner name] sent you a new cleaning agreement: [link]"
	"""
	message = language.translate("SEND_AGREEMENT_MESSAGE_SMS")
	message+= " {1}/list/{2}/agreement"
	message = message.format(cleaner_name, DOMAIN_NAME, list_id)
	send_SMS(to, message)


def send_receipt(to, cleaner_name, receipt_id):
	"""
	@param {int | str} to 		- phonenumber to send message to
	@param {str} cleaner_name 	- cleaner that created agreement 
	@param {str} receipt_id 	- id of receipt for which to send link

	Sends message: "[cleaner name] has finished cleaning your place! [link]"
	"""
	message = language.translate("SEND_RECEIPT_MESSAGE_SMS")
	message+= "\n{1}/receipt/{2}"
	message = message.format(cleaner_name, DOMAIN_NAME, receipt_id)
	send_SMS(to, message)






