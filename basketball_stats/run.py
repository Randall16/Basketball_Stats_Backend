

import boto3
import credentials

from dynamo_database import *
from models import *

''' Use this file to run sample queries against db '''


session = boto3.Session(
    aws_access_key_id=credentials.DYNAMO_IAM_ACCESS_KEY_ID,
    aws_secret_access_key=credentials.DYNAMO_IAM_SECRET_KEY,
    region_name=credentials.REGION_NAME
)

db = session.resource('dynamodb')


#create_basketball_archive_database(db)

table = db.Table('basketball_archive')


update_player_info_by_letter('b', table)
item = table.get_item(
    Key={
        PRIMARY_KEY: 'abrinal01',
        SORT_KEY: 'info'
    }
)
item = item['Item']
print(item)

del item[SORT_KEY]
pinfo = PlayerInfo(**item)
print(pinfo.colleges)

#table.delete()