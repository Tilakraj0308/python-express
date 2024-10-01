data = '''POST / HTTP/1.1
User-Agent: PostmanRuntime/7.36.1
Accept: */*
Postman-Token: 2cc031da-c172-477f-a055-6051634de12c
Host: localhost:5000
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: multipart/form-data; boundary=--------------------------682866928807036364858448
Content-Length: 383

----------------------------682866928807036364858448
Content-Disposition: form-data; name="key1"

value1
----------------------------682866928807036364858448
Content-Disposition: form-data; name="key2"

value2
----------------------------682866928807036364858448
Content-Disposition: form-data; name="key3"

value3
----------------------------682866928807036364858448--

'''

print(data.split('\n'))
boundary = data.split('boundary=')[1].split('\n')[0]
print("-------------------------------------------------")
print(boundary)
print("-------------------------------------------------")
params = '\n'.join('\n'.join('\n'.join(data.split(boundary+'\n')[2:]).split('--'+boundary+'--')).split('\n\n'))
req_params = {}
print(params)
for param in params.split('--'):
    keyValue = param.split(';')[1].split('\n')
    key = keyValue[0].split('=')[1]
    value = keyValue[1]
    req_params[key] = value
print(req_params)