# WechatSpider

# 代理的实现

setting.py文件

    ITEM_PIPELINES = {
        'mySpider.pipelines.MyspiderPipeline': 300,
        'scrapy_redis.pipelines.RedisPipeline': 400
    }

middlewares.py文件

    import base64
    class ProxyMiddleware(object):
        # overwrite process request
        def process_request(self, request, spider):
            # Set the location of the proxy
            request.meta['proxy'] = "http://117.48.201.187:16816"

            print('正在使用 117.48.201.187:16816')

            # Use the following lines if your proxy requires authentication
            proxy_user_pass = b"1228919065:lstvsmev"
            # setup basic authentication for the proxy
            encoded_user_pass = base64.b64encode(proxy_user_pass).decode('utf-8')
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass