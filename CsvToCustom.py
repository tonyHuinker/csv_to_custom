
import csv
import ConfigParser
from Ehop import Ehop


###############################################################
######## Variables                                     ########
###############################################################

vars_file = "vars.cfg"

# Load Vars
config = ConfigParser.ConfigParser()
config.read(vars_file)
eh_host = config.get("DEFAULT","eh_host")          # Extrahop Host
csv_file = config.get("DEFAULT","datafile")        # CSV File to load
api_key = config.get("DEFAULT", "api_key")

###############################################################
######## Program Start                                 ########
###############################################################

eh = Ehop(host=eh_host,apikey=api_key)

print "opening" + csv_file
with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        deviceID = 0
        indice = 0
        for cell in row:
            if indice == 0:
                print "Creating Custom Device named " + str(cell)
                body = '{ "author": "api script", "description": "", "disabled": false, "extrahop_id": "", "name": "'+cell+'" }'
                resp = eh.api_request("POST", "customdevices", body=body)
                location = resp.getheader('location')
                deviceID = location[location.rfind('/')+1:]
            if indice > 0:
                print "Adding criteria...." + str(cell)
                body = '{ "custom_device_id": '+deviceID+', "ipaddr": "'+cell+'"}'
                eh.api_request("POST", "customdevices/"+deviceID+"/criteria", body=body)

            indice = indice + 1
