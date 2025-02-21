```markdown
# TypeScript 类名检查与替换脚本

## 介绍
该 Python 脚本用于检查 TypeScript 文件中的类名是否与文件名匹配，并在不匹配时提供警告或自动修正类名。

---

## 依赖库
该脚本仅依赖 Python 内置库：
- `os`：用于文件操作和遍历目录
- `re`：用于正则表达式匹配类名
- `argparse`（未使用但可以拓展）：用于命令行参数解析

---

## 颜色代码定义
```python
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
```
- **COLOR_RED**：用于标记错误信息
- **COLOR_GREEN**：用于成功信息
- **COLOR_RESET**：用于重置颜色，避免影响终端显示

---

## 1. `get_class_name(content)`

### 功能：
从 TypeScript 文件的内容中提取 `export default class` 关键字后面的类名。

### 参数：
- `content`（str）：文件内容字符串

### 返回：
- `类名`（str）：如果匹配成功
- `None`：如果未找到匹配项

### 代码：
```python
def get_class_name(content):
    match = re.search(r'export default class\s+(\w+)', content)
    return match.group(1) if match else None
```

### 示例：
```python
content = "export default class MyClass { }"
print(get_class_name(content))  # 输出：MyClass
```

---

## 2. `get_file_name(file_path)`

### 功能：
从文件路径中提取文件名（去掉扩展名）。

### 参数：
- `file_path`（str）：文件路径

### 返回：
- `文件名`（str）：去除扩展名后的文件名

### 代码：
```python
def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]
```

### 示例：
```python
file_path = "/path/to/MyClass.ts"
print(get_file_name(file_path))  # 输出：MyClass
```

---

## 3. `print_mismatch_error(class_name, file_name, file_path)`

### 功能：
打印类名与文件名不匹配的错误信息，并显示文件路径。

### 参数：
- `class_name`（str）：文件中的类名
- `file_name`（str）：文件名（去掉扩展名）
- `file_path`（str）：文件完整路径

### 代码：
```python
def print_mismatch_error(class_name, file_name, file_path):
    print(f"{COLOR_RED}Error:{COLOR_RESET} Class name '{COLOR_RED}{class_name}{COLOR_RESET}' "
          f"does not match file name '{COLOR_GREEN}{file_name}{COLOR_RESET}' "
          f"in file: {os.path.abspath(file_path)}")
```

### 示例：
```python
print_mismatch_error("WrongClass", "RightClass", "/path/to/RightClass.ts")
```
**输出**
```
Error: Class name 'WrongClass' does not match file name 'RightClass' in file: /path/to/RightClass.ts
```

---

## 4. `replace_class_name(content, file_name)`

### 功能：
将 TypeScript 文件中的类名替换为文件名。

### 参数：
- `content`（str）：文件内容
- `file_name`（str）：文件名（不含扩展名）

### 返回：
- `新的文件内容`（str）

### 代码：
```python
def replace_class_name(content, file_name):
    return re.sub(r'(export default class\s+)(\w+)', fr'\1{file_name}', content)
```

### 示例：
```python
content = "export default class OldClass { }"
new_content = replace_class_name(content, "NewClass")
print(new_content)  # 输出：export default class NewClass { }
```

---

## 5. `check_and_replace_class_name(file_path, replace=False)`

### 功能：
检查 TypeScript 文件的类名是否与文件名匹配，并根据 `replace` 参数决定是否自动修正。

### 参数：
- `file_path`（str）：TypeScript 文件路径
- `replace`（bool）：是否自动修正类名（默认为 `False`）

### 代码：
```python
def check_and_replace_class_name(file_path, replace=False):
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
```

### 示例：
```python
check_and_replace_class_name("WrongClass.ts", True)
```
如果 `WrongClass.ts` 中的类名是 `WrongClass`，但文件名是 `CorrectClass.ts`，则类名会被自动修正为 `CorrectClass`。

---

## 6. `traverse_directory(directory, replace=False)`

### 功能：
遍历目录，检查所有 `.ts` 文件的类名，并可选地修正错误。

### 参数：
- `directory`（str）：要遍历的目录路径
- `replace`（bool）：是否自动修正类名（默认为 `False`）

### 代码：
```python
def traverse_directory(directory, replace=False):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ts'):
                file_path = os.path.join(root, file)
                check_and_replace_class_name(file_path, replace)
```

### 示例：
```python
traverse_directory("./src", True)
```
**效果**
- 遍历 `./src` 目录下的所有 `.ts` 文件
- 检查类名是否匹配文件名
- `replace=True` 时，自动修正不匹配的类名

---

## 7. `__main__` 入口

### 功能：
当脚本作为独立程序运行时，默认会遍历当前目录并自动修正类名。

### 代码：
```python
if __name__ == "__main__":
    current_directory = os.getcwd()
    traverse_directory(current_directory, True)
```

### 运行方式：
```sh
python script.py
```
**默认行为**
- 遍历当前目录下的所有 `.ts` 文件
- 自动修正不匹配的类名

---

## 总结

### 主要功能：
1. **检查 TypeScript 类名** 是否与文件名匹配
2. **错误提示** 当类名与文件名不匹配时
3. **自动修正** 类名，使其与文件名一致
4. **遍历整个目录** 并对所有 `.ts` 文件执行检查或修正

### 适用场景：
- 确保 TypeScript 文件中的类名符合文件命名规范
- 统一代码风格，避免类名与文件名不匹配的问题

---
**💡 提示**
- 若仅想检查类名是否匹配，可将 `replace=False`
- 若想自动修正类名，使用 `replace=True`