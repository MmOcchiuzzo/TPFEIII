import boto3
import botocore
from decimal import Decimal
import json
import uuid
import os
import platform

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('CorporateData')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)
print("Script ejecutando en CPU [%s] OS(%s) platform(%s) release(%s) node(%s) machine(%s)" % 
(uuid.getnode(),os.name,platform.system(),platform.release(),platform.node(),platform.machine()))
uniqueID = uuid.uuid4()
print(uniqueID)
print("Session ID (%s)" % (uniqueID)) 
response = table.get_item(
    Key={
        'id': 'UADER-FCyT-IS2'
    }
)
item = response['Item']
print(item)


"""
        Updates the quality rating of a movie in the table by using an arithmetic
        operation in the update expression. By specifying an arithmetic operation,
        you can adjust a value in a single request, rather than first getting its
        value and then setting its new value.

        :param title: The title of the movie to update.
        :param year: The release year of the movie to update.
        :param rating_change: The amount to add to the current rating for the movie.
        :return: The updated rating.
"""
for item in response['Item']:
        print(item)

x = {
	"sede" : response['Item']['sede'],
	"domicilio" : response['Item']['domicilio'],
	"localidad" : response['Item']['localidad'],
	"provincia" : response['Item']['provincia']
}
print("Python object x")
print(x)
y=json.dumps(x)
print(y)

newid=20
newid=response['Item']['idreq']
newid=newid+1
print("updating newid to %d" % (newid))
try:
	response = table.update_item(
                Key={"id": "UADER-FCyT-IS2"},
                UpdateExpression="set idreq = :r",
                ExpressionAttributeValues={":r": Decimal(str(newid))},
                ReturnValues="UPDATED_NEW",
            )
except botocore.exceptions.ClientError as err:
		print("error accediendo tabla %s Error [%s,%s]" % (table.name,err.response["Error"]["Code"],err.response["Error"]["Message"]))
		raise
else:
		print(response["Attributes"])




