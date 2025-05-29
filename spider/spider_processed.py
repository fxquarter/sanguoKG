import html

# 读取原始文件
with open('sanguo.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 解码HTML实体
text = html.unescape(text)

# 替换<br>和<br />为换行符
text = text.replace('<br>', '\n').replace('<br />', '\n')

# 替换不间断空格
text = text.replace('\xa0', ' ')

# 去除多余的换行符
text = text.replace('\n\n', '\n')

# 写入新的文件
with open('sanguo_clean.txt', 'w', encoding='utf-8') as f:
    f.write(text)