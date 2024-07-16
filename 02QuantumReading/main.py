import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
from novel import Novel

def shrink(content) -> str:
    if not isinstance(content, str):
        raise TypeError('content must be str.')

    messages = [{'role': 'system', 'content': '你是一个小说阅读助手，帮助用户对小说内容进行精简，不要输出对文章内容的总结和观点，但需要对以下内容的细节进行保留：数字、方位、时间、地点、修炼设定、武器设定、辅助工具设定、人物设定、势力设定、魂兽设定、技能设定、魂技设定、魂导器设定、战斗细节、主要情节'},
                {'role': 'user', 'content': content }]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        return 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        )

title_start = '第二百四十八章 新老战队与新规则（下）'
title_end = ''
page = 0
with open(r'02QuantumReading\output.txt', 'a') as outputIo:
    with Novel(r'01Data\原著\斗罗大陆2绝世唐门.txt') as novel:
        start = False
        for (title, content) in novel:
            page = page + 1
            if not start and (not title_start or title_start in title):
                print('start.')
                start = True
            if title_end and title_end in title:
                break
            if not start:
                print(f'skip {page} {title}')
            else:
                print(f'shrink {page} {title}\n')
                content2 = shrink(content)
                outputIo.write(f'{title}\n\n')
                outputIo.write(content2)
                outputIo.write('\n\n')
                print(content2)
                print('\n')
print('end.')