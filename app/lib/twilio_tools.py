#********************************************************************************
#--------------------------------------------------------------------------------
#
#	Significance Labs
#	Brooklyn, NYC
#
# 	Author: Alexandra Berke (aberke)
# 	Written: June 2014
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

import config


client = TwilioRestClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
NUMBER = config.TWILIO_NUMBER



def send_SMS(to, body):
	""" 
	Sends SMS message to 'to' number with message 'body'
	"""
	try:
		client.messages.create(to=to, from_=NUMBER, body=body)
	except TwilioRestException as e:
		if e.code == 21211:
			raise Exception(str(to + " is not a valid phonenumber"))
		else:
			raise e


def send_booking_confirmations(cleaner, booking):
	""" Send SMS confirmation to both cleaner and client regarding new booking 
			cleaner and booking are both dictionaries
			booking contains the time/duration/rate information
	"""
	# TODO - get time/duration/address/cost from booking dictionary
	time = "July 10, 12pm"
	duration = "3 hours"
	client_name = "Aoife Byrne"
	cleaner_name = cleaner['name']
	address = "43 Midwood Street, NT 11225"
	cost = "$70"

	cleaner_msg = "You have a new CleanSlate appointment.\nTime: {0}\nDuration: {1}\nClient Name: {2} \nAddress: {3}.".format(time, duration, client_name, address) 
	client_msg = "You have a confirmed CleanSlate appointment with {0}.\nTime: {1}\nDuration: {2}\nCost: {3}".format(cleaner_name, time, duration, cost)

	send_SMS(cleaner['phonenumber'], cleaner_msg)
	send_SMS(booking['phonenumber'], client_msg)







