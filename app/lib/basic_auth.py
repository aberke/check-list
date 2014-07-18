#********************************************************************************
#--------------------------------------------------------------------------------
#
#
#   HTTP Basic Auth Flask snippet
#   By Armin Ronacher
#
#
#--------------------------------------------------------------------------------
#*********************************************************************************


from functools import wraps
from flask import request, Response

import config


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == config.BASIC_AUTH_USERNAME and password == config.BASIC_AUTH_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    access_denied_HTML, 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


access_denied_HTML = ("<div style='text-align:center;font-family:Arial;margin-top:50px;'>"
                        "<h3>You need the username/password combination to get backstage.</h3>"
                        "<p>Just ask Alex!</p>"
                    "</div>")








