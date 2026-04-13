import os
import time
import logging
from pycomm3 import LogixDriver
from pycomm3.exceptions import CommError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("EdgePyComm3")

PLC_IP_ADDRESS = os.getenv("PLC_IP", "192.168.1.10")
TAG_TO_READ = os.getenv("TAG_READ", "Motor_Speed")
TAG_TO_WRITE = os.getenv("TAG_WRITE", "Motor_Start")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 5))

def main():
    logger.info(f"Iniciando aplicação de comunicação direta com CLP no IP: {PLC_IP_ADDRESS}")
    
    while True:
        try:
            logger.info(f"Tentando conectar ao CLP em {PLC_IP_ADDRESS}...")
            with LogixDriver(PLC_IP_ADDRESS) as plc:
                logger.info(f"Conectado com sucesso! Produto: {plc.info.get('product_name', 'Desconhecido')}")
                logger.info(f"Revisão de Firmware: {plc.info.get('revision', 'Desconhecida')}")
                
                while True:
                    logger.debug(f"Lendo tag: {TAG_TO_READ}")
                    leitura = plc.read(TAG_TO_READ)
                    
                    if leitura.error:
                        logger.error(f"Erro ao ler tag {TAG_TO_READ}: {leitura.error}")
                    else:
                        logger.info(f"Valor lido ({TAG_TO_READ}): {leitura.value}")
                        
                        if isinstance(leitura.value, (int, float)) and leitura.value > 1000:
                            logger.info(f"Velocidade alta detectada. Escrevendo True na tag {TAG_TO_WRITE}")
                            escrita = plc.write(TAG_TO_WRITE, True)
                            if escrita.error:
                                logger.error(f"Erro ao escrever tag {TAG_TO_WRITE}: {escrita.error}")
                            else:
                                logger.info(f"Escrita bem sucedida na tag {TAG_TO_WRITE}")
                    
                    time.sleep(POLL_INTERVAL)
                    
        except CommError as e:
            logger.error(f"Erro de comunicação com o CLP: {e}")
            logger.info("Aguardando 10 segundos antes de tentar reconectar...")
            time.sleep(10)
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            logger.info("Aguardando 10 segundos antes de tentar reconectar...")
            time.sleep(10)
        except KeyboardInterrupt:
            logger.info("Aplicação encerrada pelo usuário.")
            break

if __name__ == "__main__":
    main()
