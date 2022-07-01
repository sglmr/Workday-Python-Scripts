import requests
import xml.etree.ElementTree as ET


class Get_References:
    def __init__(
        self, id_type=None, username=None, password=None, tenant=None, location_url=None
    ):

        # Default empty things:
        self.references = dict()
        self.reference_ids = self.references.keys()

        # Default things
        self.ns = {"wd": "urn:com.workday/bsvc"}
        self.filter_count = 999

        self.id_type = id_type
        self.username = username
        self.password = password
        self.tenant = tenant
        self.location_url = location_url

    def _soap_request(self, page=1):
        """Creates the SOAP request Envelope(Header, Body)

        :param page: Page # for response filter, defaults to 1
        :type page: int, optional
        :return: SOAP envelope
        :rtype: str
        """

        return f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <env:Envelope   xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" 
                        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <env:Header>
            <wsse:Security env:mustUnderstand="1">
                <wsse:UsernameToken>
                    <wsse:Username>{self.username}@{self.tenant}</wsse:Username>
                    <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{self.password}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
            </env:Header>
            <env:Body>
                <wd:Get_References_Request xmlns:wd="urn:com.workday/bsvc" wd:version="v38.0">
                        <wd:Request_Criteria>
                            <wd:Reference_ID_Type>{self.id_type}</wd:Reference_ID_Type>
                        </wd:Request_Criteria>
                    <wd:Response_Filter>
                        <wd:Page>{page}</wd:Page>
                        <wd:Count>{self.filter_count}</wd:Count>
                    </wd:Response_Filter>
                </wd:Get_References_Request>
            </env:Body>
        </env:Envelope>
    """.strip()

    def get_references(self, id_type=None):
        """Orchestrates requesting reference IDs of specified type from Workday

        :param id_type: reference ID type to request, defaults to None
        :type id_type: str, optional
        """
        if id_type:
            self.id_type = id_type
        self._send_soap_request()

    def _send_soap_request(self):
        """Processes the SOAP requests with Workday,
        handles pagination if > than self.filter_count entries exist.
        Calls self._parse_soap_response() to format the responses.
        """
        self._page = 0
        self._pages = 1

        while self._page < self._pages:
            # Get response from Workday
            r = requests.post(
                self.location_url, data=self._soap_request(page=self._page + 1)
            )
            r.raise_for_status()
            self._parse_soap_response(response=r)

    def _parse_soap_response(self, response):
        """Parses Workday SOAP requests to store data into lists or dicts.

        :param response: A single Workday SOAP request response.
        :type response: str
        """
        # Parse XML
        root = ET.fromstring(response.text)

        # Page info from pages
        self._pages = int(
            root.find(".//wd:Response_Results/wd:Total_Pages", self.ns).text
        )
        self._page = int(root.find(".//wd:Response_Results/wd:Page", self.ns).text)

        # Fill in dictionary with references data
        for node in root.findall(".//wd:Reference_ID_Data", self.ns):
            key = node.find("wd:ID", self.ns).text
            value = node.find("wd:Referenced_Object_Descriptor", self.ns).text
            self.references[key] = value
