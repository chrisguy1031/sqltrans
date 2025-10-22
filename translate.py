import os
from openai import OpenAI
import time

def convert_sql_server_to_oracle(input_sql_file_path: str):
    """
    读取SQL Server存储过程文件，通过DeepSeek API转换为Oracle语法并保存。
    
    参数:
        input_sql_file_path (str): 输入的SQL Server存储过程文件路径。
    """
    # 输出文件路径
    output_oracle_file_dir = "./output"
    if not os.path.exists(output_oracle_file_dir):
        os.makedirs(output_oracle_file_dir)
    
    # 保持原文件名，添加_oracle后缀
    original_filename = os.path.basename(input_sql_file_path)
    output_filename = original_filename.replace(".sql", "_oracle.sql")
    output_oracle_file_path = os.path.join(output_oracle_file_dir, output_filename)

    # 1. 读取SQL Server存储过程文件
    try:
        with open(input_sql_file_path, 'r', encoding='utf-8') as file:
            sql_server_procedure = file.read()
        
        # 如果文件内容为空，跳过处理
        if not sql_server_procedure.strip():
            print(f"文件 {input_sql_file_path} 为空，跳过处理")
            return False
            
        print(f"已成功读取SQL Server存储过程文件：{input_sql_file_path}")
    except Exception as e:
        print(f"读取文件 {input_sql_file_path} 时出错：{e}")
        return False

    # 2. 准备调用DeepSeek API
    model = "deepseek-chat"
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not deepseek_api_key:
        print("错误: 未设置DEEPSEEK_API_KEY环境变量")
        return False
    
    client = OpenAI(
        api_key=deepseek_api_key,
        base_url="https://api.deepseek.com/v1"
    )

    # 3. 读取提示词文件
    try:
        with open("prompt.txt", 'r', encoding='utf-8') as file:
            system_prompt = file.read()
    except Exception as e:
        print(f"读取提示词文件时出错：{e}")
        return False
    
    # 构建用户提示词
    user_prompt = f"""
        请将以下SQL Server的存储过程代码转换为Oracle 26ai兼容的存储过程语法。

        SQL Server存储过程代码：
        ```sql
        {sql_server_procedure}
        ```
        请按照提示词中的要求进行转换，并只输出转换后的Oracle存储过程代码。
        """

    try:
        # 调用DeepSeek API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=False
        )
        oracle_procedure = response.choices[0].message.content
        print(f"已通过DeepSeek API完成 {original_filename} 的SQL转换")
    except Exception as e:
        print(f"调用DeepSeek API处理 {original_filename} 时出错：{e}")
        return False

    # 4. 清理API返回内容
    if oracle_procedure:
        if "```sql" in oracle_procedure:
            oracle_procedure = oracle_procedure.split("```sql")[1].split("```")[0].strip()
        elif "```" in oracle_procedure:
            oracle_procedure = oracle_procedure.split("```")[1].split("```")[0].strip()
    else:
        print(f"API返回内容为空: {original_filename}")
        return False

    # 5. 将转换后的Oracle存储过程写入文件
    try:
        with open(output_oracle_file_path, 'w', encoding='utf-8') as file:
            file.write(oracle_procedure)
        print(f"已成功生成Oracle存储过程文件：{output_filename}")
        return True
    except Exception as e:
        print(f"写入文件 {output_filename} 时出错：{e}")
        return False