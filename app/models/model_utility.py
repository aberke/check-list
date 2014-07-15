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
#********************************************************************************
#--------------------------------------------------------------------------------



from datetime import datetime 


def stamp_last_modified(data):
	"""
	cleaners, lists, and rooms collections all have a last_modified field 
	that should be updated with each insertion and update 
	"""
	data['last_modified'] = str(datetime.utcnow())
	return data
