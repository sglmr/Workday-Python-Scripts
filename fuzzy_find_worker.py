import requests


def get_references(
    tenant_id,
    username,
    password,
    refence_id_type="Employee_ID",
    page=1,
    count=900,
    v="36.1",
):
    soap_request = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <env:Envelope
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <env:Header>
            <wsse:Security env:mustUnderstand="1">
                <wsse:UsernameToken>
                    <wsse:Username>{username}@{tenant_id}</wsse:Username>
                    <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{password}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </env:Header>
        <env:Body>
            <wd:Get_References_Request xmlns:wd="urn:com.workday/bsvc" wd:version="v{v}">
                <wd:Request_Criteria>
                    <wd:Reference_ID_Type>{reference_id_type}</wd:Reference_ID_Type>
                </wd:Request_Criteria>
                <wd:Response_Filter>
                    <wd:Page>{page}</wd:Page>
                    <wd:Count>{count}</wd:Count>
                </wd:Response_Filter>
            </wd:Get_References_Request>
        </env:Body>
    </env:Envelope>
    """

    return soap_request
