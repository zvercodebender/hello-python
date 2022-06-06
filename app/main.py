# Import SDK
from rox.server.rox_server import Rox
from rox.server.rox_options import RoxOptions
from rox.server.flags.rox_flag import RoxFlag
from rox.core.entities.rox_string import RoxString
from rox.core.entities.rox_int import RoxInt
from rox.core.entities.rox_double import RoxDouble

from flask import Flask

import sys, os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
import GetConfig

################################################################################################
# Create Roxflags in the Flags container class
class Flags:
    def __init__(self):
        #Define the feature flags
        self.enableTutorial = RoxFlag(False)
        self.titleColors = RoxString('black', ['black', 'blue', 'green', 'yellow'])
        self.page = RoxInt(1, [1, 2, 3])
        self.percentage = RoxDouble(99.9, [10.5, 50.0, 99.9])

flags = Flags()
config = GetConfig.GetConfig( "/app/config/app.properties" )


# Register the flags container
#Rox.register('zvercodebender-hello-python', flags)
Rox.register( config.getProperty( "application", "flags" ) , flags)

# Setup the environment key & configuration_fetched_handler in the options object
options = RoxOptions(
    configuration_fetched_handler=lambda o:
        print("applied-from=%s creation-date=%s has-changes=%s error=%s" % (o.fetcher_status , o.creation_date , o.has_changes , o.error_details)  )
)

#cancel_event = Rox.setup("62052a2c1642474b171709dc", options).result();
cancel_event = Rox.setup( config.getProperty( "token", "flags" ) , options).result();

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

@app.route("/")
def hello():
    Rox.fetch()
    print('color is {}'.format(flags.titleColors.get_value()))
    return "<html><body>Hello Cloudbees! <br><h1 style=\"color:" + flags.titleColors.get_value() + ";\">#GoTeam!</h1></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
