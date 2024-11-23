import sys
from smsQueue import *

if __name__ == '__main__':

    if sys.argv[1] == 'IPTV':

        result = iptv_sms.apply_async(queue='iptv', args=["10"])
        print(result)
        print(result.get(timeout=1))

