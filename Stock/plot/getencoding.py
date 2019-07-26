from pip._vendor import chardet
# 获取文件编码类型


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

if __name__ == '__main__':
    pass


