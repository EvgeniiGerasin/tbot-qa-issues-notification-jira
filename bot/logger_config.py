import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="bot.log"),
        logging.StreamHandler()
    ]
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name=name)
