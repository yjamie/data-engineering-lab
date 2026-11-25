import logging
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,

        # See: https://docs.python.org/3/library/logging.html#logrecord-attributes
        format=("%(asctime)s | %(levelname)s | %(name)s: %(message)s"),

        datefmt="%Y/%m/%d %I:%M:%S %p",

        # See: https://docs.python.org/3/library/logging.handlers.html
        handlers=[
            logging.FileHandler("logs/elt.log"),
            logging.StreamHandler()
        ]
    )
