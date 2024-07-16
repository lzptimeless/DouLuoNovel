import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
from novel import Novel

def shrink(content, pre_simple_content) -> tuple[bool, str]:
    if not isinstance(content, str):
        raise TypeError('content must be str.')
    append_msg = ''
    if pre_simple_content:
        append_msg = f'。为了确保结果逻辑通顺，可以参考上一章的简要信息：{pre_simple_content}'
    messages = [{'role': 'system', 'content': '你是一个小说阅读助手，帮助用户对小说内容进行精简，不要输出对文章内容的总结和观点，但需要对以下内容的细节进行保留：数字、方位、时间、地点、修炼设定、武器设定、辅助工具设定、人物设定、势力设定、魂兽设定、技能设定、魂技设定、魂导器设定、战斗细节、主要情节' + append_msg},
                {'role': 'user', 'content': content }]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        return (True, response.output.choices[0].message.content)
    else:
        return (False, f'Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}')

title_start = '第三百八十四章 拯救，南水水（上）'
title_end = ''
page = 0
pre_simple_content = ''
with open(r'02QuantumReading\output.txt', 'a', encoding='utf8') as outputIo:
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
                success, shrink_content = shrink(content, pre_simple_content)
                if success:
                    pre_simple_content = shrink_content
                else:
                    pre_simple_content = ''
                outputIo.write(f'{title}\n\n')
                outputIo.write(shrink_content)
                outputIo.write('\n\n')
                if page % 10 == 0:
                    outputIo.flush()
                print(shrink_content)
                print('\n')
print('end.')