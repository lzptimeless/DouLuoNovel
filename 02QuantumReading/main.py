import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
from novel import Novel
import os

# 调用通义AI对小说内容进行精简
def shrink(content, pre_simple_content) -> tuple[bool, str]:
    if not isinstance(content, str):
        raise TypeError('content must be str.')
    append_msg = ''
    if pre_simple_content:
        append_msg = f'为了确保结果逻辑通顺，可以参考上一章的简要信息：{pre_simple_content}'
    messages = [{'role': 'system', 'content': '你是一个小说阅读助手，帮助用户对小说内容进行精简，不要输出对文章内容的总结和观点，但需要对以下内容的细节进行保留：数字、方位、时间、地点、修炼设定、武器设定、辅助工具设定、人物设定、势力设定、魂兽设定、技能设定、魂技设定、魂导器设定、战斗细节、主要情节。' + append_msg},
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

# 定义初始化变量
source_path = r'01Data\原著\斗罗大陆2绝世唐门.txt'
output_path = r'02QuantumReading\output.txt'
pre_last_title = '' # 上次最后精简的章节标题
page = 0 # 当前章节号，从1开始
pre_simple_content = '' # 上次精简的内容，用于下次精简作为参考
# 获取上次最后精简的章节标题
if os.path.exists(output_path):
    with Novel(output_path) as simple_novel:
        for (title, content) in simple_novel:
            pre_last_title = title
# 开始精简
with open(output_path, 'a', encoding='utf8') as outputIo:
    with Novel(source_path) as novel:
        start = False
        for (title, content) in novel:
            page = page + 1 # 计算当前章节号
            # 寻找上次精简的章节并设置start标识
            if not start:
                if not pre_last_title:
                    start = True
                elif pre_last_title in title:
                    pre_last_title = ''
            if not start:
                print(f'skip {page} {title}') # 跳过之前已经精简过章节
            else:
                print(f'shrink {page} {title}\n') # 打印当前精简章节
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