import logging
import os

LOG_FILE = os.path.join(os.getcwd(), "log.txt")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("rag_logger")