import json
import uuid
import hmac
import hashlib
import requests

#parameters send to MoMo get get payUrl
# endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
# partnerCode = "MOMONZWN20200513"
# accessKey = "aLGGNpsO3HcSPkqQ"
# serectkey = "w84mB5zTLehWMUqPNvnWuvqg5S2DkUfH"
# orderInfo = "test"
# returnUrl = "https://momo.vn/return"
# notifyurl = "https://dummy.url/notify"
# amount = "50000"
# orderId = str(uuid.uuid4())
# requestId = str(uuid.uuid4())
# requestType = "captureMoMoWallet"
# # pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
# extraData = "merchantName=;merchantId="

#before sign HMAC SHA256 with format
#partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
# rawSignature = "partnerCode="+partnerCode+"&accessKey="+accessKey+"&requestId="+requestId+"&amount="+amount + \
#     "&orderId="+orderId+"&orderInfo="+orderInfo+"&returnUrl=" + \
#     returnUrl+"&notifyUrl="+notifyurl+"&extraData="+extraData


#print("--------------------RAW SIGNATURE----------------")
#print(rawSignature)

#json object send to MoMo endpoint
# data = {
#     'partnerCode': partnerCode,
#     'accessKey': accessKey,
#    	'requestId': requestId,
#    	'amount': amount,
#    	'orderId': orderId,
#    	'orderInfo': orderInfo,
#    	'returnUrl': returnUrl,
#    	'notifyUrl': notifyurl,
#    	'extraData': extraData,
#    	'requestType': requestType,
#    	'signature': signature
# }
#print("--------------------JSON REQUEST----------------\n")
# data = json.dumps(data)
# response = requests.post(endpoint, data=data, json={
#                          'Content-Type': 'application/json'})

# #print("--------------------JSON response----------------\n")
# response_data = response.content.decode("utf-8")
# json_response = json.loads(response_data)
# payUrl = json_response['payUrl']
# orderId = json_response['orderId']
# print(payUrl)

serectkey = "w84mB5zTLehWMUqPNvnWuvqg5S2DkUfH"


partnerCode = "MOMONZWN20200513"
accessKey = "aLGGNpsO3HcSPkqQ"
requestId = "c2c7a4d3-a6c6-453b-bff4-72f39d96f89b"
amount = "600000"
orderId = "67973b99-eab9-4bd0-80cf-2eefd2eb7419"
orderInfo = "Thanh toán thẻ tập"
orderType = "momo_wallet"
transId = "2318322982"
message = "Success"
localMessage = "Thành công"
responseTime = "2020-06-02 16:49:52"
errorCode = "0"
payType = "qr"
extraData = "merchantName=;merchantId="

raw = "partnerCode={partnerCode}&accessKey={accessKey}&requestId={requestId}&amount={amount}&orderId={orderId}&orderInfo={orderInfo}&orderType={orderType}&transId={transId}&message={message}&localMessage={localMessage}&responseTime={responseTime}&errorCode={errorCode}&payType={payType}&extraData={extraData}".format(
    partnerCode=partnerCode,
   	accessKey=accessKey,
   	requestId=requestId,
   	amount=amount,
   	orderId=orderId,
   	orderInfo=orderInfo,
   	orderType=orderType,
   	transId=transId,
   	message=message,
   	localMessage=localMessage,
   	responseTime=responseTime,
   	errorCode=errorCode,
   	payType=payType,
   	extraData=extraData
)
#signature
h = hmac.new(serectkey.encode(),
             raw.encode(), hashlib.sha256)
signature = h.hexdigest()
print('=---------------------------------------=')
print(signature)
print('=---------------------------------------=')
