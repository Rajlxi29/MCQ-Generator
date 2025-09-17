import os
from datetime import datetime
import logging
File = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
file_path = os.path.join(os.getcwd(), "logs")

os.makedirs(file_path, exist_ok = True)

LOGFILE = os.path.join(file_path, File)
logging.basicConfig(
    level = logging.INFO,
    filename = LOGFILE,
    format = "[%asctime] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)