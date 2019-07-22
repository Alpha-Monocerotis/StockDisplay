from pip._vendor import chardet
# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

if __name__ == '__main__':
    with open('../../templates/sample.html', mode='r') as f:
        splited = f.read().split('<div id="ff472dc419ca4afe879d12de8263bd35" style="width:2000px;height:600px;"></div>')
        head_and_plot = splited[0]
        tail = '<div id="ff472dc419ca4afe879d12de8263bd35" style="width:2000px;height:600px;"></div>' + splited[1]
    with open('../../templates/samples.html', mode='w') as f:
        added = '''<form method="post" action="/stock">
						<label>
						课程名称
                        </label>
                         <select name="stock-name" id="stock-id">
                            <option value ="请选择">请选择</option>
                            {% for course in courses %}
                            <option value ={{ stock.file }}>{{ stock.name }}</option>
                            {% endfor %}
                         </select>
                        <div class="text-center" style="margin-top: 20px">
                        <button type="submit">
                            插入
                        </button>
                        </div>
                        </form>'''
        f.write(head_and_plot + added + tail)
        print(tail)


