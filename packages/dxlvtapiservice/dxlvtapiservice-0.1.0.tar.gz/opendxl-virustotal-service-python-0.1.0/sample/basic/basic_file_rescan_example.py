# This sample invokes and displays the results of a VirusTotal "file rescan" via DXL.
#
# See: https://www.virustotal.com/en/documentation/public-api/#rescanning-files

import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlclient.message import Message, Event, Request
from dxlbootstrap.util import MessageUtils

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    # Invoke 'file rescan' method on service
    request_topic = "/opendxl-virustotal/service/vtapi/file/rescan"
    req = Request(request_topic)
    MessageUtils.dict_to_json_payload(req, {"resource": "7657fcb7d772448a6d8504e4b20168b8"})
    res = client.sync_request(req, timeout=30)

    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        # Display results
        res_dict = MessageUtils.json_payload_to_dict(res)
        print MessageUtils.dict_to_json(res_dict, pretty_print=True)
    else:
        print "Error invoking service with topic '{0}': {1} ({2})".format(
            request_topic, res.error_message, res.error_code)
