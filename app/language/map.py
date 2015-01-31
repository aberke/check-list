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
# 	/language/map.py
#
# Contains the actual translation data
# Translate data comes from a publicly published Google Spreadsheet
# Initially contains empty map
#
# {
# 	keyname: {
# 		en: "english translation",
# 		es: "spanish translation",
# 		... for column/language in spreadsheet
# 	},
# 	... for row/keyname in spreadsheet
# }
#

# building the map.yaml file
# grep for keys in the source:
# `grep -R \{\{ '(.*)' \| translate . | grep -ow '[A-Z_]\+' | sort | uniq >> keys.txt`
# and then build dictionary with the key as the en: and es: values.
# then go through app and replace the en with the appropriate english.
#	Google documentation for accessing spreadsheet data:
#		https://developers.google.com/gdata/samples/spreadsheet_sample
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

#import requests
import config
import os
import yaml
from collections import defaultdict

# autovivification:
# http://en.wikipedia.org/wiki/Autovivification
# essentially, allows you easily dynamically build dictionaries.
Tree = lambda: defaultdict(Tree)
# map of translations kept in "cache"
map = Tree()

def get_map():
	if map:
		return map
	return build_map()

def build_map():
	# re-initialize map
	map = Tree()

	# get pwd
	script_dir = os.path.dirname(__file__)

	# load all supported languages.
	for lang in config.SUPPORTED_LANGUAGES:
		# relative to pwd
		rel_path = "./translations/{0}.yaml".format(lang)
		# yaml format:
		# KEY_NAME: "value"

		translation_path = os.path.join(script_dir, rel_path)
		yaml_string = open(translation_path)
		lang_map = yaml.load(yaml_string)
		yaml_string.close()
		for key,value in lang_map.iteritems():
			map[key][lang]=value # autovivification in action.

	return map

map = build_map()