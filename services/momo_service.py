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


class MoMoResponseService:
    def __init__(self, requestId, amount, orderId, orderInfo, orderType, transId, message, localMessage, responseTime, errorCode, payType):
        self.partnerCode = settings.MOMO_PARTNER_CODE
        self.accessKey = settings.MOMO_ACCESS_KEY
        self.requestId = requestId
        self.amount = amount
        self.orderId = orderId
        self.orderInfo = orderInfo
        self.orderType = orderType
        self.transId = transId
        self.message = message
        self.localMessage = localMessage
        self.responseTime = responseTime
        self.errorCode = errorCode
        self.payType = payType
        self.extraData = "merchantName=;merchantId="

    def signature(self):
        raw = "partnerCode={partnerCode}&accessKey={accessKey}&requestId={requestId}&amount={amount}&orderId={orderId}&orderInfo={orderInfo}&orderType={orderType}&transId={transId}&message={message}&localMessage={localMessage}&responseTime={responseTime}&errorCode={errorCode}&payType={payType}&extraData={extraData}".format(
            partnerCode=self.partnerCode,
            accessKey=self.accessKey,
            requestId=self.requestId,
            amount=self.amount,
            orderId=self.orderId,
            orderInfo=self.orderInfo,
            orderType=self.orderType,
            transId=self.transId,
            message=self.message,
            localMessage=self.localMessage,
            responseTime=self.responseTime,
            errorCode=self.errorCode,
            payType=self.payType,
            extraData=self.extraData)
        h = hmac.new(settings.MOMO_SECRET_KEY.encode(),
                     raw.encode(), hashlib.sha256)
        signature = h.hexdigest()
        return signature
