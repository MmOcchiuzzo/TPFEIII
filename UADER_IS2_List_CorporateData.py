import boto3
import json
from decimal import Decimal

def decimal_default(obj):
    """Función para convertir objetos Decimal a float."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def list_corporate_data():
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('CorporateData')
        response = table.scan()  # Obtiene todos los elementos de la tabla
        return response['Items']  # Devuelve los elementos en formato de lista
    except Exception as e:
        print(f"Error al listar los datos de CorporateData: {e}")
        return []  # Retorna una lista vacía en caso de error

if __name__ == '__main__':
    data = list_corporate_data()
    print(json.dumps(data, default=decimal_default, indent=4))  # Imprime los datos en formato JSON"""

"""def check_credentials():
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            print("Access Key:", credentials.access_key)
            print("Secret Key:", credentials.secret_key)
            print("Token:", credentials.token)
            return True
        else:
            print("No credentials found.")
            return False
    except Exception as e:
        print("Error:", e)
        return False

check_credentials()

def check_dynamodb_access():
    try:
        # Crea un recurso DynamoDB
        dynamodb = boto3.resource('dynamodb')
        
        # Intenta listar las tablas
        tables = dynamodb.tables.all()
        print("Tablas disponibles en DynamoDB:")
        for table in tables:
            print(table.name)
    except Exception as e:
        print("Error al acceder a DynamoDB:", e)

check_dynamodb_access()
"""