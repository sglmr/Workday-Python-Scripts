import requests
import os, sys
import base64
import config

env = config.tenant    # Ex: 'tenant1'
user = config.user     # Ex: 'johndo@company.com'
pw = config.pw         # Ex: 'superSecretPassword1!'


endpoints = {
    "human_resources": "https://wd2-impl-services1.workday.com/ccx/service/Human_Resources?wsdl",
}
session = requests.session()


def _soap_head(tenant, username, password):
    return  '''
        <env:Header>
            <wsse:Security env:mustUnderstand="1">
                <wsse:UsernameToken>
                    <wsse:Username>{u}@{t}</wsse:Username>
                    <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{p}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </env:Header>
    '''.format(u=username, t=tenant, p=password)

def _change_person_photo(employee, photo_64):
    return '''
        <wd:Change_Person_Photo_Request xmlns:wd="urn:com.workday/bsvc" wd:version="v31.0">
    <!--Optional:-->
    <wd:Business_Process_Parameters>
        <!--Optional:-->
        <wd:Auto_Complete>true</wd:Auto_Complete>
        <!--Optional:-->
        <wd:Run_Now>true</wd:Run_Now>
    </wd:Business_Process_Parameters>
    <wd:Person_Photo_Data>
        <!--Optional:-->
        <wd:Person_Reference>
            <!--Zero or more repetitions:-->
            <wd:ID wd:type="Employee_ID">{e}</wd:ID>
        </wd:Person_Reference>
        <wd:Photo_Data>
            <!--Optional:-->
            <wd:Filename>string.jpg</wd:Filename>
            <wd:File>{f}</wd:File>
        </wd:Photo_Data>
    </wd:Person_Photo_Data>
</wd:Change_Person_Photo_Request>

    '''.format(e=employee, f=photo_64)

def _full_soap(header, body):
    return '''
        <?xml version="1.0" encoding="UTF-8"?>
        <env:Envelope   xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" 
                        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            {h}
            <env:Body>{b}</env:Body>
        </env:Envelope>
    '''.format(h=header, b=body)


# Create B64 Encoded string for photo
test_photo = os.path.join(sys.path[0], 'test_photo.jpg')
employee = '0000000'
with open (test_photo, 'rb') as f:
    p64 = base64.b64encode(f.read())


# Creat Soap Message Parts
soap_head = soap_head = _soap_head(tenant=env, username=user, password=pw)
soap_body = _change_person_photo(employee=employee, photo_64=p64.decode("utf-8"))
# soap_body = _import_photos(employee=employee, photo_64=p64.decode("utf-8"))
full_soap = _full_soap(header=soap_head, body=soap_body).strip()

response = requests.post(endpoints['human_resources'], data=full_soap)
print(response.text)
