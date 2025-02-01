import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="./Bank/application.log",
    filemode="a",
    encoding="utf-8"
)

def log(func):
    def wrapper(*args):
        client_ip = args[0].client.client_ip
        logging.debug(f"From '{client_ip}' called '{func.__name__}' with args: {args}")
        try:
            result = func(*args)
            logging.debug(f"From '{client_ip}' results of '{func.__name__}' are: '{result}'")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper