from django.conf import settings
import json
import hmac
import hashlib
import requests
import codecs
import urllib.parse


class MoMoService:
    def __init__(self, orderInfo, returnUrl, notifyUrl, amount, orderId, requestId):
        self.signature = None
        self.partnerCode = settings.MOMO_PARTNER_CODE
        self.accessKey = settings.MOMO_ACCESS_KEY
        self.orderInfo = orderInfo
        self.returnUrl = returnUrl
        self.notifyUrl = notifyUrl
        self.amount = str(amount)
        self.orderId = orderId
        self.requestId = requestId
        self.requestType = "captureMoMoWallet"
        self.extraData = "merchantName=;merchantId="

    def call(self):
        self.signature = self.__signature()
        data = {
            'partnerCode': self.partnerCode,
            'accessKey': self.accessKey,
            'requestId': self.requestId,
            'amount': str(self.amount),
            'orderId': self.orderId,
            'orderInfo': self.orderInfo,
            'returnUrl': self.returnUrl,
            'notifyUrl': self.notifyUrl,
            'extraData': self.extraData,
            'requestType': self.requestType,
            'signature': self.signature
        }
        data = json.dumps(data)
        response = requests.post(settings.MOMO_END_POINT, data=data, json={
                                 'Content-Type': 'application/json'})
        return response

    def __signature(self):
        rawSignature = "partnerCode="+self.partnerCode+"&accessKey="+self.accessKey+"&requestId="+self.requestId+"&amount="+self.amount + \
            "&orderId="+self.orderId+"&orderInfo="+self.orderInfo+"&returnUrl=" + \
            self.returnUrl+"&notifyUrl="+self.notifyUrl+"&extraData="+self.extraData
        h = hmac.new(settings.MOMO_SECRET_KEY.encode(),
                     rawSignature.encode(), hashlib.sha256)
        signature = h.hexdigest()
        return signature
