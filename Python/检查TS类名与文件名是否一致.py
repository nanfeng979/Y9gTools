import os
import re
import argparse

# 定义颜色代码
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

def get_class_name(content):
    """
    从文件内容中提取类名。

    :param content: 文件内容字符串
    :return: 类名（如果找到），否则返回 None
    """
    match = re.search(r'export default class\s+(\w+)', content)
    return match.group(1) if match else None

def get_file_name(file_path):
    """
    从文件路径中提取文件名（不带扩展名）。

    :param file_path: 文件路径
    :return: 文件名（不带扩展名）
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def print_mismatch_error(class_name, file_name, file_path):
    """
    打印类名与文件名不匹配的错误信息。

    :param class_name: 类名
    :param file_name: 文件名
    :param file_path: 文件路径
    """
    print(f"{COLOR_RED}Error:{COLOR_RESET} Class name '{COLOR_RED}{class_name}{COLOR_RESET}' "
          f"does not match file name '{COLOR_GREEN}{file_name}{COLOR_RESET}' "
          f"in file: {os.path.abspath(file_path)}")

def replace_class_name(content, file_name):
    """
    替换文件内容中的类名为文件名。

    :param content: 文件内容字符串
    :param file_name: 文件名（不带扩展名）
    :return: 替换后的文件内容
    """
    return re.sub(r'(export default class\s+)(\w+)', fr'\1{file_name}', content)

def check_and_replace_class_name(file_path, replace=False):
    """
    检查并替换文件中的类名。

    :param file_path: 文件路径
    :param replace: 是否替换类名（默认为 False）
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        class_name = get_class_name(content)
        if class_name:
            file_name = get_file_name(file_path)
            if class_name != file_name:
                print_mismatch_error(class_name, file_name, file_path)
                if replace:
                    new_content = replace_class_name(content, file_name)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"{COLOR_GREEN}Replaced class name '{class_name}' with '{file_name}' in file: {file_path}{COLOR_RESET}")

def traverse_directory(directory, replace=False):
    """
    遍历目录并检查每个 TypeScript 文件中的类名。

    :param directory: 要遍历的目录
    :param replace: 是否替换类名（默认为 False）
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ts'):
                file_path = os.path.join(root, file)
                check_and_replace_class_name(file_path, replace)

if __name__ == "__main__":
    current_directory = os.getcwd()
    traverse_directory(current_directory, True)