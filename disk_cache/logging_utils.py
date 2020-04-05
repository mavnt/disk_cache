PROJECT_NAME = "disk_cache"
LEVEL = "INFO"
try:
    import colorlog

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s: %(message)-100s[%(module)s:%(lineno)d]"
        )
    )

    logging = colorlog.getLogger(PROJECT_NAME)
    logging.setLevel(LEVEL)
    logging.addHandler(handler)
except ModuleNotFoundError:
    import logging

    logging.basicConfig(
        format="%(levelname)-8s: %(message)-100s[%(module)s:%(lineno)d]"
    )
    logging = logging.getLogger(PROJECT_NAME)
    logging.setLevel(LEVEL)

logger = logging
