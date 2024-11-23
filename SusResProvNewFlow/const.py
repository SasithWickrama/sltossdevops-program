from log import getLogger

voiceend = 'http://10.68.128.3:8080/spg'
crbt= 'http://10.68.198.66/SLTCrbt/ProvisionCallback.php'
iptvend='http://10.68.148.5:8082/tbms/services/TPEWebService.TPEWebServiceHttpSoap11Endpoint/'
pcrf = "http://10.68.74.5:28080/ProvisioningInterface/ProvisionPCRF?WSDL"

dbhost='172.25.1.172'
dbport=1521
dbservice='clty'
dbuser='OSSPRG'
dbpwd='prgoss456'

ldapip="10.68.74.32"
ldappwd = "o$Sld@PAdm!N"
ldapusr = "OSSUser"

logsusvoice = getLogger('susvoice', 'logs/susprov')
logsusbb = getLogger('susbb', 'logs/susprov')
logsusiptv = getLogger('susiptv', 'logs/susprov')
logresvoice = getLogger('resvoice', 'logs/resprov')
logresbb = getLogger('resbb', 'logs/resprov')
logresiptv = getLogger('resiptv', 'logs/resprov')