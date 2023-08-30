import base64
import hmac
import hashlib
from utils.Config import XF_API_ADDRESS, XF_API_SECRET, XF_API_KEY
from datetime import datetime
from time import mktime
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time


# 获取鉴权URL要求的格式化时间
def get_format_datetime():
    current_time = datetime.now()
    return format_date_time(mktime(current_time.timetuple()))


# 实时拼接时间来获取请求url
def generate_url():
    parse_result = urlparse(XF_API_ADDRESS)
    hostname = parse_result.netloc
    path = parse_result.path
    current_datetime = get_format_datetime()
    return "host: {0}\ndate: {1}\nGET {2} HTTP/1.1".format(hostname, current_datetime, path)


# 生成科大讯飞开发平台的请求签名
def generate_signature():
    url = generate_url()
    _sha = hmac.new(
        XF_API_SECRET.encode("utf-8"),
        url.encode("utf-8"),
        digestmod=hashlib.sha256).digest()
    return base64.b64encode(_sha).decode(encoding="utf-8")


# 生成科大讯飞开放平台的通用鉴权URL
def generate_authorization_url():
    current_datetime = get_format_datetime()
    hostname = urlparse(XF_API_ADDRESS).netloc
    signature = generate_signature()
    authorization_origin = f"api_key='{XF_API_KEY}'', " \
                           f"algorithm='hmac-sha256', " \
                           f"headers='host date request-line', " \
                           f"signature='{signature}''"
    authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode(encoding="utf-8")
    v = {
        "authorization": authorization,  # 上方鉴权生成的authorization
        "date": current_datetime,        # 实时生成的datetime
        "host": hostname                 # 请求的主机名，根据具体接口替换
    }
    return XF_API_ADDRESS + "?" + urlencode(v)
