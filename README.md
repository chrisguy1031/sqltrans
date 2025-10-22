# SQL Translator

## 项目介绍

SQL Translator 是一个基于 DeepSeek API 的工具，用于将 SQL Server 存储过程语法转换为 Oracle 26ai 兼容的语法。项目通过多进程并行处理，支持批量转换输入目录中的所有 SQL 文件，并输出到指定目录。

### 核心功能
1. **语法转换**：将 SQL Server 存储过程转换为 Oracle 语法。
2. **批量处理**：支持多进程并行处理多个 SQL 文件。
3. **自动化**：自动扫描输入目录并生成转换后的文件。

## 安装手册

### 依赖安装
1. 确保已安装 Python 3.12 版本。
2. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```
3. 设置环境变量 `DEEPSEEK_API_KEY`：
   ```bash
   export DEEPSEEK_API_KEY="your_api_key_here"
   ```

## 使用手册

### 目录结构
- `input/`：存放待转换的 SQL Server 存储过程文件（`.sql` 后缀）。
- `output/`：存放转换后的 Oracle 存储过程文件（自动生成）。
- `prompt.txt`：包含 DeepSeek API 的提示词，用于指导语法转换。

### 运行步骤
1. 将 SQL Server 存储过程文件放入 `input/` 目录。
2. 运行主程序：
   ```bash
   python main.py
   ```
3. 查看 `output/` 目录获取转换后的文件。

### 输出示例
```
开始处理文件: ./input/test1.sql
已成功读取SQL Server存储过程文件：./input/test1.sql
已通过DeepSeek API完成 test1.sql 的SQL转换
已成功生成Oracle存储过程文件：test1_oracle.sql
完成处理文件: ./input/test1.sql (耗时: 5.23秒)
```

## 注意事项
1. 确保 `DEEPSEEK_API_KEY` 环境变量已正确设置。
2. 输入文件必须为有效的 SQL Server 存储过程语法。
3. 输出文件的命名规则为 `原文件名_oracle.sql`。

## Docker 支持

### 使用 Docker 运行
1. 确保已安装 Docker 和 Docker Compose。
2. 构建并启动容器：
   ```bash
   export DEEPSEEK_API_KEY="your_api_key_here"
   docker-compose up
   ```
3. 容器会自动挂载 `input/` 和 `output/` 目录，转换结果将保存在 `output/` 中。

### 注意事项
- 确保宿主机上的 `input/` 和 `output/` 目录存在。
- 如果 `DEEPSEEK_API_KEY` 未设置，容器启动时会报错。