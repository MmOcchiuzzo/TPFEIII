import platform
import uuid
import boto3
from PatronSingleton import SingletonMeta
import logging
import json
from botocore.exceptions import BotoCoreError, ClientError

class CorporateLog(metaclass=SingletonMeta):
    _instance = None

    @staticmethod
    def getInstance():
        if CorporateLog._instance is None:
            CorporateLog._instance = CorporateLog()
        return CorporateLog._instance

    def __init__(self):
        self.CPUid = str(uuid.getnode())  # Almacena el UUID de la CPU
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateLog')  # Inicializa la tabla
        logging.basicConfig(level=logging.INFO)

    # Método para agregar registros a la tabla
    def post(self, uuid_session, method_name):
        cpu_data = platform.uname()
        log_entry = {
            "id": str(uuid.uuid4()),
            "uuid_session": uuid_session,
            "method": method_name,
            "cpu_name": cpu_data.node,
            "CPUid": self.CPUid,  # Asegúrate de usar la clave correcta aquí
            "timestamp": str(uuid.uuid1())
        }

        try:
            self.table.put_item(Item=log_entry)
            logging.info(f"Log inserted successfully: {log_entry}")
            return "Registro guardado correctamente en DynamoDB."
        except Exception as e:
            logging.error(f"Error inserting log entry: {e}")
            return "Error al guardar el registro en DynamoDB."

    def list(self):
        """Lista todos los registros para la CPU actual."""
        try:
            response = self.table.scan(
                FilterExpression="CPUid = :CPUid",  # Filtra por el UUID de la CPU
                ExpressionAttributeValues={":CPUid": self.CPUid}
            )
            logs = response.get('Items', [])
            logging.info(f"Logs recuperados: {logs}")  # Imprimir los logs para verificar su estructura
            return logs if logs else "No se encontraron registros para la CPU especificada."
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Error al listar los registros en DynamoDB: {error}")
            return f"Error al listar los registros en DynamoDB: {error}"

    def listar_logs_por_cpu(self):
        """Devuelve un listado de todas las entradas para la CPU actual en formato JSON."""
        logs = self.list()
        return json.dumps({"logs_por_cpu": logs}, default=str, indent=4)  # Usa `default=str` para serializar objetos que no son JSON serializables
