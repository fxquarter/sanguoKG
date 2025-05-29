import os


def remove_last_two_chars_from_filenames(directory):
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        # 构建完整的文件路径
        file_path = os.path.join(directory, filename)

        # 确保只处理文件，而不是目录
        if os.path.isfile(file_path):
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)

            # 确保文件名长度大于2，以避免去除过多字符
            if len(name) > 2:
                # 去除文件名的最后两个字符
                new_filename = name[:-2] + ext
            else:
                # 如果文件名长度不足，保持原样
                new_filename = filename

            new_file_path = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"重命名: {filename} -> {new_filename}")


# 使用示例
directory_path =r'D:\python_xuexi\三国演义\图片2' # 替换为你的文件夹路径
remove_last_two_chars_from_filenames(directory_path)
