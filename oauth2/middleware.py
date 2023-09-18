import json
import time

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from oauth2.encrypt import sign, timestamp, random_str


class OpenAPIMiddleware(MiddlewareMixin):
    """
    中间件生成Token
    """

    def process_request(self, request):
        """
        token认证
        :param request:
        :return:token
        """
        # 获取url
        url = request.get_full_path()
        # 定义一个白名单 注册登录接口 随便访问
        white_list = ['/hw']
        # 判断url在不在白名单中
        if url in white_list:
            req_sign = request.headers.get("Sign")
            if not req_sign:
                return HttpResponse('sign not found')

            calc_sign = sign(request.headers.get("Timestamps"), request.headers.get("Random"),
                             request.body.decode("utf-8"), "123456")
            if req_sign != calc_sign:
                return HttpResponse('sign is error')

            if int(time.time()) - int(request.headers.get("Timestamps")) / 1000 > 30:
                return HttpResponse('Time span exceeds 30 seconds')

            print("req_sign pass")

        return None
