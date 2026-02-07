import logging

def make_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(f"[{name}] %(asctime)s %(message)s")

    file = logging.FileHandler(f"{name}.log")
    file.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(file)
    logger.addHandler(console)

    return logger
