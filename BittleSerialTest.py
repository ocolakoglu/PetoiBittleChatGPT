
import sys

sys.path.append("..")
from ardSerial import *

if __name__ == '__main__':
    try:
        goodPorts = {}

        connectPort(goodPorts)
        if len(goodPorts) > 0:
            time.sleep(3);
            send(goodPorts, ['g', 1])
            time.sleep(1);
            send(goodPorts, ['ksit', 1])
            time.sleep(1);
            send(goodPorts, ['krest', 1])
            time.sleep(1);
            send(goodPorts, ['kzero', 1])
            closeAllSerial(goodPorts)
            logger.info("finish!")

    except Exception as e:
        logger.info("Exception")
        closeAllSerial(goodPorts)
        raise e
