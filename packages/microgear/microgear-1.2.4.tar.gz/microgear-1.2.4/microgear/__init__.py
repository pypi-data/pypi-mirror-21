import logging
__version__ = '1.2.4'

gearauthsite = "http://ga.netpie.io:8080"
gearauthrequesttokenendpoint = gearauthsite+"/api/rtoken"
gearauthaccesstokenendpoint = gearauthsite+"/api/atoken"

mgrev = "PY11k"
gearkey = None
gearsecret = None
gearalias = None
appid = None
gearname = None
accesstoken = None
requesttoken = None
client = None
scope = ""
gearexaddress = None
gearexport = None
mqtt_client = None
logger = logging.getLogger("python-microgear")
