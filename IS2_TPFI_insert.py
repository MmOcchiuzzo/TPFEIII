#*---------------------------------------------------------------------------------------------------------------
#* IS2_TPFI_insert.py
#* Programa auxiliar para verificar la inserción de registros en la tabla Log
#*
#*---------------------------------------------------------------------------------------------------------------
import boto3
import botocore
from decimal import Decimal
import json
import uuid
import os
import platform

dynamodb = boto3.resource('dynamodb')


table = dynamodb.Table('CorporateLog')

uniqueID=str(uuid.uuid4())
CPUid=str(uuid.getnode())
sessionid=str(uuid.uuid4())
ts=str(table.creation_date_time)

response = table.put_item(
           Item={
            'id': uniqueID,
            'CPUid' : CPUid,
            'sessionid' : sessionid,
            'timestamp': ts
        }
)
    
print("id=%s CPU=%s session=%s time=%s\n" % (uniqueID,CPUid,sessionid,ts))
status_code = response['ResponseMetadata']['HTTPStatusCode']
print("status code:",status_code)

