import os
import re
from io import StringIO

class Novel(object):
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__re_title = re.compile(r'^\s*(第.*章.*)\s*$')
        self.__title = ''

    def __str__(self) -> str:
        return os.path.basename(self.__file_path)
    
    def __enter__(self):
        self.__file_io = open(self.__file_path, 'r', encoding='utf8')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file_io.close()
        return
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # 获取章节标题，只有第一个标题需要执行这部分代码
        if not self.__title:
            while True:
                line = self.__file_io.readline()
                if not line:
                    raise StopIteration()
                m = self.__re_title.match(line)
                if m:
                    self.__title = m.group(1).strip()
                    break
        # 获取章节内容
        content_io = StringIO()
        while True:
            line = self.__file_io.readline()
            if not line:
                if content_io.tell() > 0:
                    title = self.__title
                    self.__title = ''
                    content_io.seek(0)
                    content = content_io.read()
                    return (title, content)
                else:
                    raise StopIteration()
            else:
                m = self.__re_title.match(line)
                if m:
                    title = self.__title
                    self.__title = m.group(1).strip()
                    content_io.seek(0)
                    content = content_io.read()
                    return (title, content)
                else:
                    content_io.write(line)