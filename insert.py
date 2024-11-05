import uuid
import boto3
import logging
from CorporateData import CorporateData  
from CorporateLog import CorporateLog    
from datetime import datetime

# Obtén la instancia única de CorporateData
corporate_data = CorporateData()
# Obtén la instancia de CorporateLog
corporate_log = CorporateLog.getInstance()

# Genera identificadores únicos
uniqueID = str(uuid.uuid4())  # ID único para el registro
CPUid = str(uuid.getnode())  # ID único de la CPU
sessionid = str(uuid.uuid4())  # ID único para la sesión

# Conectarse a la tabla 'CorporateLog' en DynamoDB
table_name = 'CorporateLog'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

# Insertamos el log en la tabla con un timestamp actual
try:
    response = table.put_item(
        Item={
            'id': uniqueID,
            'CPUid': CPUid,
            'sessionid': sessionid,
            'timestamp': str(datetime.now())  # Marca de tiempo actual
        }
    )

    # Registrar el log después de la operación
    corporate_log.post(sessionid, "insert") 

    # Muestra la información insertada
    print(f"ID={uniqueID} CPU={CPUid} Session={sessionid} Time={datetime.now()}\n")

    # Verifica el código de estado de la respuesta
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    print("Status code:", status_code)

except Exception as e:
    logging.error(f"Error inserting log into CorporateLog: {e}")
