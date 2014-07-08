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

import boto # using boto for connecting to s3

S3_URL = "https://s3.amazonaws.com"
BUCKET_NAME = 'cleaners'
ALLOWED_PIC_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])




def public_bucket_url(keyname):
	return str(S3_URL + '/' + BUCKET_NAME + '/' + keyname)


def allowed_pic(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_PIC_EXTENSIONS


def upload_pic(id, file):
	"""
	Uploads pic file to s3 bucket.  Replaces existing file if pic for id already exists.
	Returns new url to pic
	"""
	if not (file and allowed_pic(file.filename)):
		raise Exception("Invalid file uploaded")

	s3 = boto.connect_s3()
	bucket = s3.get_bucket(BUCKET_NAME)

	keyname = str('pics/' + id)

	key = bucket.new_key(keyname)
	# will rewrite file if key already exists (PUT OR POST)
	key.set_contents_from_file(file, headers=None, replace=True, cb=None, num_cb=10, policy=None, md5=None) 
	return public_bucket_url(keyname)



