JWT_SECRET_KEY = "NO6nTRKT4BsoOaDiYKiVpdIA9f3SJUgz"

#TOKEN
APP_ROUTE_TOKEN = '/sltdevops/apiServices/token'
#SMS
APP_ROUTE_SMS = '/sltdevops/apiServices/sms'
#LTE
APP_ROUTE_LTE = '/sltdevops/apiServices/lte'
#MOBITEL OCS
APP_ROUTE_RECHARGE = '/api/mobitel/reverse/recharge/'
APP_ROUTE_OFFERACTIVATE = '/api/mobitel/reverse/offerActivate/'
APP_ROUTE_CHANGEOFFERSTAT = '/api/mobitel/reverse/changeOfferStatus/'
APP_ROUTE_CHANGESTAT = '/api/mobitel/reverse/changeSubStatus/'
APP_ROUTE_BALANCEEXHAUST = '/api/mobitel/reverse/balanceExhaust/'
#PCRF
PCRF_TOKEN_URL = 'http://172.25.16.215:8085/subscribertoken'
PCRF_ADDON_CREATE_URL = 'http://172.25.16.215:8085/vasdataadd-ons/enroll'
PCRF_ADDON_VASDATA_URL = 'http://172.25.16.215:8085/dashboard/vas_data'
PCRF_ADDON_DELETE_URL = 'http://172.25.16.215:8085/vasdataadd-ons/unsubscribe'


APP_ROUTE_MAPPING = '/api/mySltOcs/mapping/'
APP_ROUTE_OFFER = '/api/mobitel/ocs/offer/'

#SMS GATEWAY
hostname="10.68.198.100"
port= 5019
system_id= "oss"
passwd = "MabL@z8/"

system_id2= "smsbot"
passwd2 = "8MW2XWqT"

system_id3= "sltpoc1"
passwd3 = "Test@123"