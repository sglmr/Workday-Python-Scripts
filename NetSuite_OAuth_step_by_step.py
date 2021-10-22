import base64
import urllib
import requests
import hashlib
import hmac

# Thank you - https://morrisdev.medium.com/netsuite-token-based-authentication-tba-342c7df56386

realm = "*realm*"
base_url = f"https://{realm}-sb1.restlets.api.netsuite.com/app/site/hosting/restlet.nl"
http_method = "POST"
script_id = "*id*"
oauth_version = "1.0"
script_deployment_id = "1"
token_id = "*token_id*"
token_secret = "token_secret*"
consumer_key = "*consumer_key*"
consumer_secret = "*consumer_secret*"

oauth_nonce = "*nonce*"
time_stamp = "*timestamp*"

# Create parameter string
data = ""
data = data + "deploy=" + script_deployment_id + "&"
data = data + "oauth_consumer_key=" + consumer_key + "&"
data = data + "oauth_nonce=" + oauth_nonce + "&"
data = data + "oauth_signature_method=" + "HMAC-SHA256" + "&"
data = data + "oauth_timestamp=" + time_stamp + "&"
data = data + "oauth_token=" + token_id + "&"
data = data + "oauth_version=" + oauth_version + "&"
data = data + "script=" + script_id

encoded_data = requests.utils.quote(data, safe="")

complete_data = "&".join(
    (http_method, requests.utils.quote(base_url, safe=""), encoded_data)
)

secret = consumer_secret + "&" + token_secret

signature = hmac.new(
    key=secret.encode("UTF-8"),
    msg=complete_data.encode("UTF-8"),
    digestmod=hashlib.sha256,
).hexdigest()

signature_b64 = base64.b64decode(signature)

print(signature_b64)
