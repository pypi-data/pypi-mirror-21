
# Import opinel
from opinel.utils import *


########################################
##### Helpers
########################################

#
# Connect to Cloudtrail
#
def connect_cloudtrail(credentials, region, silent = False):
    return connect_service('CloudTrail', credentials, region_name = region, silent = silent)

#
# Get the list of trails for a given region
#
def get_trails(cloudtrail_client):
    trails = cloudtrail_client.describe_trails()
    return trails['trailList']
