import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="./Bank/application.log",
    filemode="a",
)

def log(func):
    def wrapper(*args, **kwargs):
        client_ip = args[0].client.client_ip
        logging.debug(f"From {client_ip} called {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper