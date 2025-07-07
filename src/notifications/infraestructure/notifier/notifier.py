from logging import Logger

class Notifier:

    def __init__(self, logger: Logger):
        self.logger = logger

    async def notify_info(self,msg: str):
        self.logger.info(msg)