1.安装requests
```
pip install requests
```

2.基本请求

```
https://2.python-requests.org/en/master/

requests.request(method, url, **kwargs)：构建发送请求。method可以为：HEAD，GET，POST，PUT，PATCH，DELETE，OPTIONS。
requests.head(url, **kwargs)：发送HEAD请求。
requests.get(url, params=None, **kwargs)：发送GET请求。
requests.post(url, data=None, json=None, **kwargs)：发送POST请求。
requests.put(url, data=None, **kwargs)：发送PUT请求。
requests.patch(url, data=None, **kwargs)：发送PATCH请求。
requests.delete(url, **kwargs)：发送DELETE请求。

**kwargs参数：
params：请求中用于发送的查询字符串，可以是字典，元组列表或字节。
data：用于请求实体发送的字典，元组列表，字节或类似文件的对象。
json：用于请求实体发送的JSON序列化的Python对象。
headers：字典形式的头文件信息数据包。
cookies：字典形式或CookieJar对象形式的cookie数据。
files：字典形式的多部分编码上传。形式为{'name': file-like-objects}或{'name': file-tuple}。file-tuple可以是二元组('filename', fileobj)、三元组('filename', fileobj, 'content_type')或4元组('filename', fileobj, 'content_type', custom_headers)。'content-type'是给定文件的内容类型，custom_headers是字典，包含了文件需要的附加头信息。
auth：身份验证元组，可以是基本的、简要的或自定义的HTTP验证。
timeout：等待服务器发送数据的秒数。可以是一个浮点值，或者是(connect timeout, read timeout)元组。
allow_redirects：布尔值。是否允许GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD重定向。默认是True。
proxies：字典形式的URL代理协议映射。
verify：当为布尔值时，用于控制是否验证服务器的TLS证书。当为字符串时，必须是一个路径，这个路径指向了要使用的CA绑定。默认是True。
stream： 如果为False，立即下载响应内容。
cert：如果是字符串，则为SSL客户机证书文件的路径（.pem），如果为元组，则为(‘cert’, ‘key’)元组形式。
```

3.异常
```
exception requests.RequestException(*args, **kwargs)
exception requests.ConnectionError(*args, **kwargs)
exception requests.HTTPError(*args, **kwargs)
exception requests.URLRequired(*args, **kwargs)
exception requests.TooManyRedirects(*args, **kwargs)
exception requests.ConnectTimeout(*args, **kwargs)
exception requests.ReadTimeout(*args, **kwargs)
exception requests.Timeout(*args, **kwargs)
```

4.请求会话
```
class requests.Session

方法和属性：
auth = None：依附Request的默认身份验证。参考requests.request()的相应参数。
cert = None：参考requests.request()的相应参数。
close()：关闭所有适配，并关闭会话。
cookies = None：参考requests.request()的相应参数。
delete(url, **kwargs)：发送DELETE请求。
get(url, **kwargs)：发送GET请求。
get_adapter(url)：返回给定的URL的连接适配。
get_redirect_target(resp)：返回重定向RUI或None。
head(url, **kwargs)：发送HEAD请求。
headers = None：参考requests.request()的相应参数。
hooks = None：事件处理。
max_redirects = None：允许的最大重定向次数。默认为requests.models.DEFAULT_REDIRECT_LIMIT，即30。
merge_environment_settings(url, proxies, stream, verify, cert)：检测环境设置，并合并。
mount(prefix, adapter)：注册连接adapter到prefix。
options(url, **kwargs)：发送OPTIONS请求。
params = None：参考requests.request()的相应参数。
patch(url, data=None, **kwargs)：发送PATCH请求。
post(url, data=None, json=None, **kwargs)：发送POST请求。
prepare_request(request)：构建PreparedRequest并返回。
proxies = None：参考requests.request()的相应参数。
put(url, data=None, **kwargs)：发送PUT请求。
rebuild_auth(prepared_request, response)：重向定时重建身份验证。
rebuild_method(prepared_request, response)：重定向时修改请求方式。
rebuild_proxies(prepared_request, proxies)：重定向时重建代理。
request(method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None)：创建请求，准备并发送。
resolve_redirects(resp, req, stream=False, timeout=None, verify=True, cert=None, proxies=None, yield_requests=False, **adapter_kwargs)：返回响应或请求的生成器。
send(request, **kwargs)：发送给定的PreparedRequest。
should_strip_auth(old_url, new_url)：重定向时是否移除身份验证。
stream = None：参考requests.request()的相应参数。
trust_env = None：可信的环境代理设置。
verify = None：参考requests.request()的相应参数。
```

5.下层类
```
https://2.python-requests.org/en/master/api/#lower-level-classes
class requests.Request(method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None)
class requests.Response
```

6.更下层类
```
https://2.python-requests.org/en/master/api/#lower-lower-level-classes
class requests.PreparedRequest
class requests.adapters.BaseAdapter
class requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=0, pool_block=False)
```

7.身份验证类
```
https://2.python-requests.org/en/master/api/#authentication
class requests.auth.AuthBase
class requests.auth.HTTPBasicAuth(username, password)
class requests.auth.HTTPProxyAuth(username, password)
class requests.auth.HTTPDigestAuth(username, password)
```

8.编码
```
https://2.python-requests.org/en/master/api/#encodings
requests.utils.get_encodings_from_content(content)
requests.utils.get_encoding_from_headers(headers)
requests.utils.get_unicode_from_response(r)
```

9.Cookies
```
https://2.python-requests.org/en/master/api/#cookies
requests.utils.dict_from_cookiejar(cj)
requests.utils.add_dict_to_cookiejar(cj, cookie_dict)
requests.cookies.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
class requests.cookies.RequestsCookieJar(policy=None)
class requests.cookies.CookieConflictError
```

10.状态码
```
https://2.python-requests.org/en/master/api/#status-code-lookup
requests.codes
    100: continue
    101: switching_protocols
    102: processing
    103: checkpoint
    122: uri_too_long, request_uri_too_long
    200: ok, okay, all_ok, all_okay, all_good, \o/, ✓
    201: created
    202: accepted
    203: non_authoritative_info, non_authoritative_information
    204: no_content
    205: reset_content, reset
    206: partial_content, partial
    207: multi_status, multiple_status, multi_stati, multiple_stati
    208: already_reported
    226: im_used
    300: multiple_choices
    301: moved_permanently, moved, \o-
    302: found
    303: see_other, other
    304: not_modified
    305: use_proxy
    306: switch_proxy
    307: temporary_redirect, temporary_moved, temporary
    308: permanent_redirect, resume_incomplete, resume
    400: bad_request, bad
    401: unauthorized
    402: payment_required, payment
    403: forbidden
    404: not_found, -o-
    405: method_not_allowed, not_allowed
    406: not_acceptable
    407: proxy_authentication_required, proxy_auth, proxy_authentication
    408: request_timeout, timeout
    409: conflict
    410: gone
    411: length_required
    412: precondition_failed, precondition
    413: request_entity_too_large
    414: request_uri_too_large
    415: unsupported_media_type, unsupported_media, media_type
    416: requested_range_not_satisfiable, requested_range, range_not_satisfiable
    417: expectation_failed
    418: im_a_teapot, teapot, i_am_a_teapot
    421: misdirected_request
    422: unprocessable_entity, unprocessable
    423: locked
    424: failed_dependency, dependency
    425: unordered_collection, unordered
    426: upgrade_required, upgrade
    428: precondition_required, precondition
    429: too_many_requests, too_many
    431: header_fields_too_large, fields_too_large
    444: no_response, none
    449: retry_with, retry
    450: blocked_by_windows_parental_controls, parental_controls
    451: unavailable_for_legal_reasons, legal_reasons
    499: client_closed_request
    500: internal_server_error, server_error, /o\, ✗
    501: not_implemented
    502: bad_gateway
    503: service_unavailable, unavailable
    504: gateway_timeout
    505: http_version_not_supported, http_version
    506: variant_also_negotiates
    507: insufficient_storage
    509: bandwidth_limit_exceeded, bandwidth
    510: not_extended
    511: network_authentication_required, network_auth, network_authentication
```

11.例子演示
```
#!/usr/bin/env python
# coding=utf-8

import requests
import json


# https://2.python-requests.org/en/master/user/quickstart/、
def test_basic_requests():
    r = requests.post('http://httpbin.org/post')  # POST请求
    print '1.post: status_code =', r.status_code  # 状态码
    r = requests.put('http://httpbin.org/put')  # PUT请求
    print '2.put: status_code =', r.status_code
    r = requests.delete('http://httpbin.org/delete')  # DELETE请求
    print '3.delete: status_code =', r.status_code
    r = requests.head('http://httpbin.org/get')  # HEAD请求
    print '4.head: status_code =', r.status_code
    r = requests.options('http://httpbin.org/get')  # OPTIONS请求
    print '5.options: status_code =', r.status_code
    r = requests.get('http://httpbin.org/get')  # GET请求
    print '6.get: status_code =', r.status_code


def test_response_properties():
    r = requests.get('http://httpbin.org/get')  # GET请求
    print '1.url =', r.url  # URL
    print '2.text =', r.text  # 文本
    print '3.encoding =', r.encoding  # 编码
    print '4.content =', r.content  # 内容
    print '5.status_code =', r.status_code  # 状态码
    print '6.headers =', r.headers  # 头信息


def test_parameters():
    # GET
    payload = {'key1': 'value1', 'key2': ['value2', 'value3']}  # 参数
    headers = {'content-type': 'application/json'}  # 头信息
    r = requests.get('http://httpbin.org/get', params=payload, headers=headers)  # GET请求
    print '1.get+params+header: text =', r.text  # 文本

    r = requests.get('https://api.github.com/events', stream=True)  # 流式
    # print '2.get+stream: text =', r.text  # 文本
    # print '2.get+stream: json =', r.json()  # json格式
    print '2.get+stream: raw =', r.raw  # 原始格式

    # POST
    r = requests.post('http://httpbin.org/post', data=payload)  # POST请求，data信息
    print '3.post+data: text =', r.text

    r = requests.post('http://httpbin.org/post', data=json.dumps(payload))  # data信息
    print '4.post+data: text =', r.text

    r = requests.post('http://httpbin.org/post', json=payload)  # 通过json传递
    print '5.post+json: text =', r.text

    files = {'file': open('post_file.txt', 'rb')}
    r = requests.post('http://httpbin.org/post', files=files)  # 上传文件
    print '6.post+files: text =', r.text


def test_cookie():
    url = 'http://www.baidu.com'
    r = requests.get(url)
    print '1.cookie =', r.cookies.items()  # 拿到cookie

    url = 'http://httpbin.org/cookies'
    cookies = dict(cookies_test='cookie_test')
    r = requests.get(url, cookies=cookies)  # 把cookie上传到服务器
    print '2.text =', r.text


def test_timeout():
    try:
        r = requests.get('http://github.com', timeout=0.1)  # 等待延时0.1秒
        print 'status_code =', r.status_code
    except requests.ConnectionError as e:
        print e.message  # 异常信息


def test_session():
    # 两次打开，但设置的cookie信息拿不到
    requests.get('http://httpbin.org/cookies/set/sessioncookie/cookievalue')
    r = requests.get('http://httpbin.org/cookies')
    print '1.text =', r.text  # cookie为空

    # 同一个会话，设置的cookie信息可以拿到
    s = requests.Session()
    s.get('http://httpbin.org/cookies/set/sessioncookie/cookievalue')
    r = s.get('http://httpbin.org/cookies')
    print '2.text =', r.text

    # 同一个会话，设置关信息，可以覆盖，也可以设置None来消除
    s = requests.Session()
    s.headers.update({'header-text': 'test1'})
    r = s.get('http://httpbin.org/headers', headers={'header-text2': 'test2'})  # 如果key已经在headers中存在，会覆盖，如不要，设为None
    print '3.text =', r.text


def test_verify():
    r = requests.get('https://github.com', verify=True)  # verify=False则不验证SSL证书
    print 'status_code =', r.status_code


def test_proxy():
    proxies = {'https': 'http://xx.xx.xx.xx:xxxx'}  # 更改为有效的地址
    r = requests.post('http://httpbin.org/post', proxies=proxies)
    print 'text =', r.text


if __name__ == '__main__':
    print 'test_basic_requests' + '*' * 100
    test_basic_requests()
    print 'test_response_properties' + '*' * 100
    test_response_properties()
    print 'test_parameters' + '*' * 100
    test_parameters()
    print 'test_cookie' + '*' * 100
    test_cookie()
    print 'test_timeout' + '*' * 100
    test_timeout()
    print 'test_session' + '*' * 100
    test_session()
    print 'test_verify' + '*' * 100
    test_verify()
    print 'test_proxy' + '*' * 100
    test_proxy()


'''
输出为：

test_basic_requests****************************************************************************************************
1.post: status_code = 200
2.put: status_code = 200
3.delete: status_code = 200
4.head: status_code = 200
5.options: status_code = 200
6.get: status_code = 200
test_response_properties****************************************************************************************************
1.url = http://httpbin.org/get
2.text = {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "origin": "113.111.9.128, 113.111.9.128", 
  "url": "https://httpbin.org/get"
}

3.encoding = None
4.content = {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "origin": "113.111.9.128, 113.111.9.128", 
  "url": "https://httpbin.org/get"
}

5.status_code = 200
6.headers = {'Content-Length': '182', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff', 'Content-Encoding': 'gzip', 'Server': 'nginx', 'Connection': 'keep-alive', 'Access-Control-Allow-Credentials': 'true', 'Date': 'Fri, 12 Jul 2019 07:47:56 GMT', 'Access-Control-Allow-Origin': '*', 'Referrer-Policy': 'no-referrer-when-downgrade', 'Content-Type': 'application/json', 'X-Frame-Options': 'DENY'}
test_parameters****************************************************************************************************
1.get+params+header: text = {
  "args": {
    "key1": "value1", 
    "key2": [
      "value2", 
      "value3"
    ]
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Type": "application/json", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "origin": "113.108.131.107, 113.108.131.107", 
  "url": "https://httpbin.org/get?key2=value2&key2=value3&key1=value1"
}

2.get+stream: raw = <urllib3.response.HTTPResponse object at 0x7f9da976d4d0>
3.post+data: text = {
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "key1": "value1", 
    "key2": [
      "value2", 
      "value3"
    ]
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "35", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "json": null, 
  "origin": "113.111.9.128, 113.111.9.128", 
  "url": "https://httpbin.org/post"
}

4.post+data: text = {
  "args": {}, 
  "data": "{\"key2\": [\"value2\", \"value3\"], \"key1\": \"value1\"}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "48", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "json": {
    "key1": "value1", 
    "key2": [
      "value2", 
      "value3"
    ]
  }, 
  "origin": "113.111.9.128, 113.111.9.128", 
  "url": "https://httpbin.org/post"
}

5.post+json: text = {
  "args": {}, 
  "data": "{\"key2\": [\"value2\", \"value3\"], \"key1\": \"value1\"}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "48", 
    "Content-Type": "application/json", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "json": {
    "key1": "value1", 
    "key2": [
      "value2", 
      "value3"
    ]
  }, 
  "origin": "113.111.9.128, 113.111.9.128", 
  "url": "https://httpbin.org/post"
}

6.post+files: text = {
  "args": {}, 
  "data": "", 
  "files": {
    "file": "test"
  }, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "153", 
    "Content-Type": "multipart/form-data; boundary=238bed0f55b23f3e7aa9f6e94d629ea8", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "json": null, 
  "origin": "113.111.9.128, 113.111.9.128", 
  "url": "https://httpbin.org/post"
}

test_cookie****************************************************************************************************
1.cookie = [('BDORZ', '27315')]
2.text = {
  "cookies": {
    "cookies_test": "cookie_test"
  }
}

test_timeout****************************************************************************************************
HTTPConnectionPool(host='github.com', port=80): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x7f9da9ac8d90>, 'Connection to github.com timed out. (connect timeout=0.1)'))
test_session****************************************************************************************************
1.text = {
  "cookies": {}
}

2.text = {
  "cookies": {
    "sessioncookie": "cookievalue"
  }
}

3.text = {
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Header-Text": "test1", 
    "Header-Text2": "test2", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }
}

test_verify****************************************************************************************************
status_code = 200
test_proxy****************************************************************************************************
text = {
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "0", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.20.1"
  }, 
  "json": null, 
  "origin": "113.111.9.128, 113.111.9.128", 
  "url": "https://httpbin.org/post"
}
'''
```
