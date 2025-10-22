import os
import multiprocessing
from translate_bak import convert_sql_server_to_oracle
import time

def process_sql_file(sql_file):
    """处理单个SQL文件的函数，用于多进程调用"""
    try:
        print(f"开始处理文件: {sql_file}")
        start_time = time.time()
        
        convert_sql_server_to_oracle(sql_file)
        
        end_time = time.time()
        print(f"完成处理文件: {sql_file} (耗时: {end_time - start_time:.2f}秒)")
        return True
    except Exception as e:
        print(f"处理文件 {sql_file} 时出错: {e}")
        return False

def main():
    """主函数，使用多进程并行处理所有SQL文件"""
    input_dir = "./input"
    output_dir = "./output"
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 {input_dir} 不存在")
        return
    
    # 获取所有SQL文件
    sql_files = []
    for file in os.listdir(input_dir):
        if file.endswith(".sql"):
            sql_files.append(os.path.join(input_dir, file))
    
    if not sql_files:
        print("在input目录中没有找到SQL文件")
        return
    
    print(f"找到 {len(sql_files)} 个SQL文件需要处理")
    
    # 设置进程数（可以根据CPU核心数调整）
    # 建议设置为CPU核心数的1.5-2倍，但不要超过文件数量
    cpu_count = multiprocessing.cpu_count()
    process_count = min(cpu_count * 2, len(sql_files))
    
    print(f"CPU核心数: {cpu_count}")
    print(f"使用进程数: {process_count}")
    
    # 使用进程池并行处理
    start_time = time.time()
    
    with multiprocessing.Pool(processes=process_count) as pool:
        results = pool.map(process_sql_file, sql_files)
    
    # 统计处理结果
    successful = sum(results)
    failed = len(results) - successful
    
    total_time = time.time() - start_time
    
    print("\n" + "="*50)
    print("处理完成!")
    print(f"总文件数: {len(sql_files)}")
    print(f"成功: {successful}")
    print(f"失败: {failed}")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"平均每个文件: {total_time/len(sql_files):.2f}秒")

if __name__ == "__main__":
    main()