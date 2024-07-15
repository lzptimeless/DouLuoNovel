import re
from io import StringIO
import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0

def shrink(content):
    if not isinstance(content, str):
        raise TypeError('content参数必须是str。')

    messages = [{'role': 'system', 'content': '你是一个小说阅读助手，帮助用户对小说内容进行精简。'},
                {'role': 'user', 'content': content }]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        print(response.output.choices[0].message.content)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

re_title = re.compile(r'^\s*(第.*章).*$')
pre_title = ''
content_io = StringIO()
with open('斗罗大陆2绝世唐门.txt', 'r', encoding='utf8') as f:
    n = 0
    while n < 5:
        l = f.readline()
        m = re_title.match(l)
        if m:
            if pre_title:
                print(pre_title)
                content_io.seek(0)
                content = content_io.read()
                content_io.close()
                if content:
                    n = n + 1
                    shrink(content)

            pre_title = m.group(0)
            content_io = StringIO()
        else:
            content_io.write(l)