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
#	Base file of language module
# 	/language/__init__.py
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************

from flask import Blueprint, request, session

from app.lib.util import dumpJSON, respond500, respond200, jsonp, APIexception, JSONencoder, yellERROR
from map import get_map
import config


SUPPORTED_LANGUAGES = config.SUPPORTED_LANGUAGES
DEFAULT_LANGUAGE    = config.DEFAULT_LANGUAGE



bp = Blueprint('language', __name__, static_folder='static')





def get_language_setting():
    return session.get('language-setting', None)


def set_language_setting(value):
    if value and (value not in SUPPORTED_LANGUAGES): # value of None is for deleting language-setting
        raise APIexception(message='Attempt to set language to a value ({0}) not supported'.format(value))
    session['language-setting'] = value


def translate(keyname):
    """
    If keyname not mapped with language setting in translation map, return keyname
    TODO: Test coverage
    """
    language = get_language_setting()
    if not language:
        language = DEFAULT_LANGUAGE

    translate_map = get_map()
    try:
        return translate_map[keyname][language]
    except Exception as e:
        yellERROR('Error translating term: {0} with language: {1}\nError: {2}'.format(keyname, language, e.message))
        return keyname



#- Language Setting API --------------------------------------------------
@bp.route('/setting', methods=['POST'])
def POST_setting():
    try:
        data = JSONencoder.load(request.data)
        if 'language-setting' not in data:
            raise APIexception("POST /language/setting expects 'language-setting' in payload")
        
        set_language_setting(data['language-setting'])
        return respond200()
    except Exception as e:
        return respond500(e)


@bp.route('/setting')
@jsonp
def GET_language_setting():
    try:
        data = { 'language-setting': get_language_setting() }
        return dumpJSON(data)
    except Exception as e:
        return respond500(e)


@bp.route('/setting', methods=['DELETE'])
def DELETE_language_setting():
    """
    Clear the language setting from the session - not actually used by module
    """
    try:
        set_language_setting(None)
        return respond200()
    except Exception as e:
        return respond500(e)

#-------------------------------------------------- Language Setting API -


@bp.route('/map')
@jsonp
def GET_map():
    """
    Returns the formatted language map.
    Data pulled from google spreadsheet and then formatted as
    {
        keyname: {
          en: "english translation",
          es: "spanish translation",
          ... for column/language in spreadsheet
        },
    ... for row/keyname in spreadsheet
    }
    """
    try:
        data = get_map()
        return dumpJSON(data)
    except Exception as e:
        return respond500(e)


























