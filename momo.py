import json
import uuid
import hmac
import hashlib
import requests

#parameters send to MoMo get get payUrl
endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
partnerCode = "MOMONZWN20200513"
accessKey = "aLGGNpsO3HcSPkqQ"
serectkey = "w84mB5zTLehWMUqPNvnWuvqg5S2DkUfH"
orderInfo = "test"
returnUrl = "https://momo.vn/return"
notifyurl = "https://dummy.url/notify"
amount = "50000"
orderId = str(uuid.uuid4())
requestId = str(uuid.uuid4())
requestType = "captureMoMoWallet"
# pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
extraData = "merchantName=;merchantId="

#before sign HMAC SHA256 with format
#partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
rawSignature = "partnerCode="+partnerCode+"&accessKey="+accessKey+"&requestId="+requestId+"&amount="+amount + \
    "&orderId="+orderId+"&orderInfo="+orderInfo+"&returnUrl=" + \
    returnUrl+"&notifyUrl="+notifyurl+"&extraData="+extraData


#print("--------------------RAW SIGNATURE----------------")
#print(rawSignature)

#signature
h = hmac.new(serectkey.encode(),
             rawSignature.encode(), hashlib.sha256)
signature = h.hexdigest()

#json object send to MoMo endpoint
data = {
    'partnerCode': partnerCode,
    'accessKey': accessKey,
   	'requestId': requestId,
   	'amount': amount,
   	'orderId': orderId,
   	'orderInfo': orderInfo,
   	'returnUrl': returnUrl,
   	'notifyUrl': notifyurl,
   	'extraData': extraData,
   	'requestType': requestType,
   	'signature': signature
}
#print("--------------------JSON REQUEST----------------\n")
data = json.dumps(data)
response = requests.post(endpoint, data=data, json={
                         'Content-Type': 'application/json'})

#print("--------------------JSON response----------------\n")
response_data = response.content.decode("utf-8")
json_response = json.loads(response_data)
payUrl = json_response['payUrl']
orderId = json_response['orderId']
print(payUrl)