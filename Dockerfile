FROM ubuntu:22.04

WORKDIR /app

# 使用阿里云镜像并安装依赖
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# 使用单个最稳定的镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip config set global.timeout 1000 && \
    pip config set global.retries 10 && \
    pip install --no-cache-dir --timeout 1000 openai>=1.0.0 httpx>=0.23.0 && \
    pip install --no-cache-dir --timeout 1000 -r requirements.txt

ENV DEEPSEEK_API_KEY=""

CMD ["python3", "main.py"]