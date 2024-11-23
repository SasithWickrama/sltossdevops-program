import zeep


wsdl = 'http://creditcontrol.intranet.slt.com.lk:8080/CreditControl_SOA/CreatdiControl_SOA?WSDL'
client = zeep.Client(wsdl=wsdl)
result = client.service.update_soa_action('OSS', '123', '', '', 'COMPLETED', 'COMPLETED','','')

print(result['transaction_Status'])