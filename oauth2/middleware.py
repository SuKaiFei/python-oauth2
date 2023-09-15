from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


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
            return HttpResponse('401')
        return None
