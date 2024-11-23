
import const
from log import Logger

logger = Logger.getLogger('lte', 'logs/lte')


class Lteprov:
    def lteProv(data, ref):
        logger.info("LTE : %s" % ref + " - " + str(data))
        return data