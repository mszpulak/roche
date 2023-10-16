import logging


server_logger = logging.getLogger("server logger")


def setup_logger(server_logger):
    level = logging.DEBUG
    server_logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    server_logger.addHandler(console_handler)


setup_logger(server_logger)
