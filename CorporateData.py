import boto3
from PatronSingleton import SingletonMeta
from CorporateLog import CorporateLog
import logging
import json
from botocore.exceptions import BotoCoreError, ClientError 

class CorporateData(metaclass=SingletonMeta):
    _instance = None

    @staticmethod
    def get_instance():
        if CorporateData._instance is None:
            CorporateData._instance = CorporateData()
        return CorporateData._instance

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.log = CorporateLog.getInstance()  # Ahora debería funcionar correctamente
        logging.basicConfig(level=logging.INFO)
    
    def getData(self, uuid_session, uuid_cpu, sede_id):
        self.log.post(uuid_session, "getData")
        table = self.dynamodb.Table('CorporateData')
        response = table.get_item(Key={'id': sede_id})
        if 'Item' in response:
            return {
                "id": response['Item']['id'],
                "domicilio": response['Item']['domicilio'],
                "localidad": response['Item']['localidad'],
                "cp": response['Item']['cp'],
                "provincia": response['Item']['provincia']
            }
        else:
            return {"error": "Registro no encontrado"}

    def getCUIT(self, uuid, uuidCPU, id):
        """Retorna el CUIT de la sede."""
        try:
            table = self.dynamodb.Table('CorporateData')
            response = table.get_item(Key={'id': id})
            if 'Item' in response:
                return {"CUIT": response['Item'].get("CUIT")}
            else:
                return {"error": "Registro no encontrado"}
        except (BotoCoreError, ClientError) as error:
            return {"error": f"Error al acceder a la base de datos: {error}"}

    def getSeqID(self, uuid, uuidCPU, id):
        """Retorna un identificador de secuencia único y lo incrementa en la base de datos."""
        try:
            table = self.dynamodb.Table('CorporateData')
            response = table.get_item(Key={'id': id})
            if 'Item' in response:
                idSeq = response['Item'].get("idreq", 0) + 1
                table.update_item(
                    Key={'id': id},
                    UpdateExpression="set idreq = :val",
                    ExpressionAttributeValues={':val': idSeq}
                )
                return {"idSeq": idSeq}
            else:
                return {"error": "Registro no encontrado"}
        except (BotoCoreError, ClientError) as error:
            return {"error": f"Error al acceder a la base de datos: {error}"}

    def listar_corporate_data(self):
        """Retorna una estructura JSON con todos los campos de la tabla CorporateData."""
        try:
            table = self.dynamodb.Table('CorporateData')
            response = table.scan()  # Escanear todos los elementos de la tabla
            data = response.get('Items', [])
            return json.dumps({"corporate_data": data}, indent=4)
        except Exception as e:
            return json.dumps({"error": f"Error al acceder a la base de datos: {e}"})
