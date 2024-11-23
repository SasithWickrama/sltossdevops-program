
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta

from sme_data_incentive import Data
from sme_final_calculation import FinalCalc
from sme_retail_Incentive import Retail
from sme_revenue_incentive import Revenue
from sme_voicecommit_incentive import VoiceCommit

lstmonth = datetime.now() - relativedelta(months=4)
cmonth = lstmonth.strftime('%Y%m')


# last_month = datetime.now() - relativedelta(months=3)
# lmon = last_month.replace(day=1) - timedelta(days=1)
# pmon = lmon.replace(day=1) - timedelta(days=1)
# lastmonth = lmon.strftime('%d-%b-%Y')


#Retail.retailData(cmonth)
#Data.dataData(cmonth)
#Revenue.totalRevenue(cmonth)
#VoiceCommit.voiceCommit(cmonth)


FinalCalc.finalCal(cmonth)



