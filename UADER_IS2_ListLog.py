import json
from CorporateLog import CorporateLog
from decimal import Decimal

# Función para manejar Decimals
def custom_encoder(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convertir Decimal a float
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def list_all_logs():
    log_instance = CorporateLog.getInstance()
    logs = log_instance.listar_logs_por_cpu()  # Llama al método que lista los registros por CPU
    
    return logs

if __name__ == '__main__':
    logs = list_all_logs()  # Llama a la función y guarda el resultado
    if logs:
        print(logs)  # Imprime el resultado en formato JSON
    else:
        print("No se encontraron registros en la tabla.")




   
