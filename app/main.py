# Import SDK
#from urllib import request
from rox.server.rox_server import Rox
from rox.server.rox_options import RoxOptions
from rox.server.flags.rox_flag import RoxFlag
from rox.core.entities.rox_string import RoxString
from rox.core.entities.rox_int import RoxInt
from rox.core.entities.rox_double import RoxDouble

import logging
from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
from flask import session

import sys, os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
import GetConfig

################################################################################################
# example of a naive Logger
class MyLogger:
    def error(self, msg, ex=None):
        print('error: %s exception: %s' %(msg, ex))

    def warn(self, msg, ex=None):
        print('warn: %s' % msg)

    def debug(self, msg, ex=None):
        print('debug: %s' % msg)

################################################################################################
# Create Roxflags in the Flags container class
class Flags:
    def __init__(self):
        #Define the feature flags
        self.enableTutorial = RoxFlag(False)
        self.titleColors = RoxString('black', ['black', 'blue', 'green', 'yellow'])
        self.page = RoxInt(1, [1, 2, 3])
        self.percentage = RoxDouble(99.9, [10.5, 50.0, 99.9])
        Rox.set_custom_string_property('email', 'rbroker@cloudbees.com')

flags = Flags()
config = GetConfig.GetConfig( "/app/config/app.properties" )


# Register the flags container
Rox.register( config.getProperty( "application", "flags" ) , flags)
print("App Name: %s" % config.getProperty( "application", "flags" ) )

# Setup the environment key & configuration_fetched_handler in the options object

options = RoxOptions(
    logger=MyLogger(),
    configuration_fetched_handler=lambda o:
        print("applied-from=%s creation-date=%s has-changes=%s error=%s" % (o.fetcher_status , o.creation_date , o.has_changes , o.error_details)  )
)

cancel_event = Rox.setup( config.getProperty( "token", "flags" ) , options).result();
print("Token: %s" % config.getProperty( "token", "flags" ) )

# Boolean flag example
print('enableTutorial is {}'.format(flags.enableTutorial.is_enabled()))

# String flag example
print('color is {}'.format(flags.titleColors.get_value()))

# Int flag example
print('page is {}'.format(flags.page.get_value()))

# Double flag example
print('percentage is {}'.format(flags.percentage.get_value()))


################################################################################################
#   Main Loop
#
app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

logger = logging.getLogger('werkzeug')

@app.route("/success")
def success():
   return 'welcome ' + session["email"] + "</p><a href=\"/\">Home</a>"

@app.route("/")
def hello():
    Rox.fetch()
    logger.info('color is {}'.format(flags.titleColors.get_value()))
    return "<html><body>Hello Cloudbees with Github Action! <br><h1 style=\"color:" + flags.titleColors.get_value() + ";\">#GoTeam!</h1></body></html>"

@app.route("/getemail",methods = ['POST', 'GET'])
def getemail():
   if request.method == 'POST':
        logger.info('GetEMail POST')
        email = request.form['email']
        session['email'] = request.form['email']
        logger.info('email = ' + email)
        Rox.set_custom_string_property('email', email)
        return redirect(url_for('success'))
   else:
        return render_template('getemail.html')
    #   return redirect(url_for('success',email = 'rbroker@cloudbees.com'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
