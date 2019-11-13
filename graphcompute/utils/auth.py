# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64
import urllib
import time

class Credentials(object):
    def __init__(self, access_key_id, access_key_secret):
        self.access_key_id = access_key_id.strip()
        self.access_key_secret = access_key_secret.strip()

    def __str__(self):
        return "access_key_id: [%s], access_key_secret: [%s]" % (self.access_key_id, self.access_key_secret)

class Auth(object):
    def __init__(self, credentials):
        if not isinstance(credentials, Credentials):
            raise Exception("please provide corrent credentials")

        self._credentials = credentials

    def gen_user(self):
        return self._credentials.access_key_id

    def gen_remote_credentials(self):
        m_dict = dict()
        m_dict["accesskey"]=self._credentials.access_key_id
        m_dict["timestamp"] = str(int(time.time()*1000))
        m_dict["signature_type"] = "HMAC-MD5"
        m_dict["version"] = "1.0"

        base_str=""
        for k in sorted(m_dict.keys()):
            base_str += k
            base_str += "="
            base_str += m_dict[k]
            base_str += "&"

        sign = self._gen_sign(m_dict)
        m_dict["signature"] = sign

        template_str = "?accessKeyId=%s&signatureMethod=HMAC-MD5&version=1.0&timestamp=%s&signature=%s"

        remote_credentials = template_str % (m_dict["accesskey"], m_dict["timestamp"], sign)

        return remote_credentials


    def _gen_sign(self, m_dict):
        base_str=""
        access_key_secret = self._credentials.access_key_secret
        for k in sorted(m_dict.keys()):
            base_str += k
            base_str += "="
            base_str += m_dict[k]
            base_str += "&"

        base_str = base_str[:-1]
        txt = hmac.new(access_key_secret, base_str, hashlib.md5)
        sign = base64.b64encode(txt.digest()).decode()
        return urllib.quote(sign)


