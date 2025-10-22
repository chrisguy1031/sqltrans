import os
from openai import OpenAI  # 使用与OpenAI兼容的DeepSeek SDK

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
    output_oracle_file_path = os.path.join(output_oracle_file_dir, os.path.basename(input_sql_file_path).replace(".sql", "_oracle.sql"))

    # 1. 读取SQL Server存储过程文件
    try:
        with open(input_sql_file_path, 'r', encoding='utf-8') as file:
            sql_server_procedure = file.read()
        print(f"已成功读取SQL Server存储过程文件：{input_sql_file_path}")
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return

    # 2. 准备调用DeepSeek API
    model = "deepseek-chat"
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    client = OpenAI(
        api_key=deepseek_api_key,
        base_url="https://api.deepseek.com/v1"  # DeepSeek API基础端点 :cite[2]
    )

    # 构建转换提示词
    with open(input_sql_file_path, 'r', encoding='utf-8') as file:
            user_prompt = file.read()
    system_prompt = "你是一个专业的数据库工程师，精通SQL Server和Oracle的存储过程语法转换。"

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
        print("已通过DeepSeek API完成SQL转换。")
    except Exception as e:
        print(f"调用DeepSeek API时出错：{e}")
        return

    # 3. 清理API返回内容（确保只提取SQL代码，去除可能的Markdown标记）
    # 某些API返回可能包含Markdown的代码块标记，这里尝试去除它们。
    if "```sql" in oracle_procedure: # type: ignore
        oracle_procedure = oracle_procedure.split("```sql")[1].split("```")[0].strip() # type: ignore
    elif "```" in oracle_procedure: # type: ignore
        oracle_procedure = oracle_procedure.split("```")[1].split("```")[0].strip() # type: ignore

    # 4. 将转换后的Oracle存储过程写入文件
    try:
        with open(output_oracle_file_path, 'w', encoding='utf-8') as file:
            file.write(oracle_procedure) # type: ignore
        print(f"已成功生成Oracle存储过程文件：{output_oracle_file_path}")
    except Exception as e:
        print(f"写入文件时出错：{e}")
        return

# 使用示例
if __name__ == "__main__":
    # 替换为你的实际路径和API密钥
    input_file = "./input/test1.sql"
    
    convert_sql_server_to_oracle(input_file)