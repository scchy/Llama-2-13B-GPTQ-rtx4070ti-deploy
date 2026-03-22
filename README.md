# Qwen2.5-GPTQ RTX 4070 Ti 部署指南

针对 **NVIDIA RTX 4070 Ti (12GB GDDR6X)** 优化的 **Qwen2.5** 本地部署方案，使用 vLLM 提供 OpenAI 兼容的 API 服务。

> 🎉 阿里通义千问 Qwen2.5，中文理解能力强劲，7B/14B 参数即可满足大多数场景！

---

## 🎮 硬件要求

| 规格 | 详情 | 说明 |
|------|------|------|
| GPU | NVIDIA RTX 4070 Ti | 12GB GDDR6X |
| 显存带宽 | 21 Gbps | 高速显存访问 |
| Tensor Cores | 第三代 | 加速推理 |
| 算力 | ~40 TFLOPS (FP16) | 充足计算性能 |

### 支持模型配置

| 模型 | 参数量 | 量化 | 显存占用 | 上下文长度 | 适用场景 |
|------|--------|------|----------|------------|----------|
| Qwen2.5-7B-Instruct-GPTQ-Int4 | 7B | GPTQ Int4 | ~6GB | 24K | 日常使用、推荐配置 |
| Qwen2.5-14B-Instruct-GPTQ-Int4 | 14B | GPTQ Int4 | ~10-11GB | 8K | 高质量生成 |
| Qwen2.5-Coder-7B-Instruct-GPTQ-Int4 | 7B | GPTQ Int4 | ~6GB | 24K | 代码生成 |
| Qwen2.5-Coder-7B-Instruct-AWQ | 7B | AWQ | ~6GB | 24K | 代码生成(更快) |

---

## 📁 项目结构

```
.
├── README.md              # 项目说明
├── requirements.txt       # Python依赖
├── download_model.py      # 模型下载脚本
├── service.sh            # 启动vLLM服务
├── test_vllm.py          # 本地模型加载测试
└── test_service.py       # API服务测试
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建conda环境
conda create -n llm python=3.10 -y
conda activate llm

# 安装依赖
pip install -r requirements.txt
```

### 2. 下载模型

```bash
# 设置模型下载目录（可选，默认使用环境变量 SCC_DISK）
export SCC_DISK=/path/to/model/cache

# 下载模型
python download_model.py
```

> 默认下载 `Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4`，如需其他模型请修改脚本中的 `model_name`

### 3. 启动服务

```bash
# 赋予执行权限
chmod +x service.sh

# 启动服务（默认 7B 模型，24K 上下文）
./service.sh
```

服务启动后，API 端点为 `http://localhost:8088`

### 4. 测试服务

```bash
# 测试API服务
python test_service.py
```

---

## ⚙️ 配置说明

### service.sh 关键参数

```bash
--model /path/to/model              # 模型路径
--served-model-name qwen2.5-7B      # 服务模型名称
--quantization gptq                 # 量化方式 (gptq/gptq_marlin/awq)
--dtype float16                     # 数据类型
--max-model-len 24576               # 最大上下文长度
--gpu-memory-utilization 0.88       # GPU显存利用率
--max-num-seqs 1                    # 最大并发序列数
--enable-auto-tool-choice           # 启用工具调用
--tool-call-parser hermes           # 工具调用解析器
--port 8088                         # 服务端口
```

### 显存优化建议

| 显存限制 | max-model-len | gpu-memory-utilization | max-num-seqs |
|----------|---------------|------------------------|--------------|
| 12GB (宽松) | 8192 | 0.92 | 2 |
| 12GB (平衡) | 24576 | 0.88 | 1 |
| 12GB (紧凑) | 2048 | 0.95 | 1 |

---

## 🔧 API 使用示例

### OpenAI 兼容接口

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8088/v1", api_key="sk-test")

# 简单对话
response = client.chat.completions.create(
    model="qwen2.5-7B",
    messages=[{"role": "user", "content": "你好"}],
    max_tokens=100
)
print(response.choices[0].message.content)

# 流式输出
stream = client.chat.completions.create(
    model="qwen2.5-7B",
    messages=[{"role": "user", "content": "讲个故事"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

# 工具调用
response = client.chat.completions.create(
    model="qwen2.5-7B",
    messages=[{"role": "user", "content": "读取 /tmp/test.txt"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "read_file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                }
            }
        }
    }],
    tool_choice="auto"
)
```

### curl 测试

```bash
# 简单对话
curl -X POST http://localhost:8088/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-7B",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
  }'
```

---

## 📊 性能参考

在 RTX 4070 Ti 上的实测性能：

| 模型 | 量化 | 上下文 | 吞吐量 | 首token延迟 |
|------|------|--------|--------|-------------|
| Qwen2.5-7B-Instruct | GPTQ Int4 | 2K | ~45 tokens/s | ~0.3s |
| Qwen2.5-7B-Instruct | GPTQ Int4 | 8K | ~35 tokens/s | ~0.5s |
| Qwen2.5-7B-Instruct | GPTQ Int4 | 24K | ~20 tokens/s | ~1.2s |
| Qwen2.5-14B-Instruct | GPTQ Int4 | 2K | ~25 tokens/s | ~0.5s |

---

## 🐛 故障排除

### 显存不足 (OOM)

```bash
# 降低上下文长度
--max-model-len 2048

# 降低显存利用率
--gpu-memory-utilization 0.85

# 减少并发
--max-num-seqs 1

# 使用 AWQ 量化（更快更省显存）
--quantization awq
```

### 模型下载失败

```bash
# 使用 ModelScope 镜像（国内推荐）
python download_model.py

# 或手动从 HuggingFace 下载
# 需先安装: pip install huggingface_hub
```

### 量化方式不匹配

| 模型后缀 | 正确量化参数 |
|----------|--------------|
| -GPTQ-Int4 | `gptq` 或 `gptq_marlin` |
| -AWQ | `awq` |

---

## 📚 相关资源

- [Qwen2.5 官方文档](https://qwen.readthedocs.io/)
- [vLLM 文档](https://docs.vllm.ai/)
- [GPTQ 量化说明](https://github.com/PanQiWei/AutoGPTQ)

---

## 📄 License

本项目仅供学习和研究使用。模型遵循各自的原版许可证。
