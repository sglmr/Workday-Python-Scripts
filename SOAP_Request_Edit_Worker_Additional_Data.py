import requests

isu = '*ISU*'
pw = '*password'
tenant = '*tenant*'

url = f'https://wd2-impl-services1.workday.com/ccx/service/{tenant}/Staffing/v33.2' # Sandbox/impl
url = f'https://services1.myworkday.com/ccx/service/{tenant}/Staffing/v33.2' # Prod


worker = 'test_worker'
effective_date = '2020-12-10'
vendor_compliant = 'true'
vendor_status = 'ON_TRACK'


message = f"""
<soapenv:Envelope xmlns:bsvc="urn:com.workday/bsvc" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header>
      <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
         <wsse:UsernameToken >
            <wsse:Username>{isu}@{tenant}</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{pw}</wsse:Password>
         </wsse:UsernameToken>
      </wsse:Security>
   </soapenv:Header>
   <soapenv:Body>
      <bsvc:Edit_Worker_Additional_Data_Request bsvc:version="v33.2">
         <bsvc:Business_Process_Parameters>
            <bsvc:Auto_Complete>true</bsvc:Auto_Complete>
            <bsvc:Run_Now>true</bsvc:Run_Now>
         </bsvc:Business_Process_Parameters>
         <bsvc:Worker_Custom_Object_Data>
            <bsvc:Effective_Date>{effective_date}</bsvc:Effective_Date>
            <bsvc:Worker_Reference>
               <bsvc:ID bsvc:type="WID">{worker}</bsvc:ID>
            </bsvc:Worker_Reference>
            <bsvc:Business_Object_Additional_Data xmlns:cus="urn:com.workday/tenants/super/data/custom">
               <cus:vendorTrainingStatus>
                  <cus:vendorCompliant>{vendor_compliant}</cus:vendorCompliant>
                  <cus:vendorEngagement>
                    <cus:ID cus:type="ExtendedAlias">{vendor_status}</cus:ID>
                  </cus:vendorEngagement>
              	</cus:vendorTrainingStatus>
            </bsvc:Business_Object_Additional_Data>
         </bsvc:Worker_Custom_Object_Data>
      </bsvc:Edit_Worker_Additional_Data_Request>
   </soapenv:Body>
</soapenv:Envelope>"""



r = requests.post(url=url,data=message)

print(f'{r.text}')
