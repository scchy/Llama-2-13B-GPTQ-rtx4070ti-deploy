# 错误退出
set -e
export CUDA_HOME=/usr/local/cuda

# /home/scc/anaconda3/envs/LLM/bin/python -m vllm.entrypoints.openai.api_server \
#     --model /home/scc/sccWork/devData/sccDisk/model_weight/Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4 \
#     --served-model-name qwen2.5-14B \
#     --quantization gptq_marlin \
#     --dtype float16 \
#     --max-model-len 2048 \
#     --gpu-memory-utilization 0.92 \
#     --max-num-seqs 2 \
#     --trust-remote-code \
#     --enforce-eager \
#     --port 8088

# pkill -9 -f "VLLM|vllm|api_server"
# 启动 Qwen2.5-7B 模型
echo "🚀 启动 Qwen2.5-7B (24K 上下文)..."
/home/scc/anaconda3/envs/LLM/bin/python -m vllm.entrypoints.openai.api_server \
    --model /home/scc/sccWork/devData/sccDisk/model_weight/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4 \
    --served-model-name qwen2.5-7B \
    --quantization gptq \
    --dtype float16 \
    --max-model-len 24576 \
    --gpu-memory-utilization 0.88 \
    --max-num-seqs 1 \
    --trust-remote-code \
    --enforce-eager \
    --enable-auto-tool-choice \
    --tool-call-parser hermes \
    --port 8088

# pythonic
# /home/scc/anaconda3/envs/LLM/bin/python -m vllm.entrypoints.openai.api_server \
#     --model  /home/scc/sccWork/devData/sccDisk/model_weight/Qwen/Qwen2.5-Coder-7B-Instruct-AWQ \
#     --served-model-name qwen2.5-7B \
#     --quantization awq \
#     --dtype float16 \
#     --max-model-len 24576 \
#     --gpu-memory-utilization 0.88 \
#     --max-num-seqs 1 \
#     --trust-remote-code \
#     --enforce-eager \
#     --enable-auto-tool-choice \
#     --tool-call-parser hermes \
#     --port 8088
    # --chat-template ./qwen_tool_template.jinja \
  
# 服务启动后的操作
echo "✅ 服务已启动在 http://localhost:8088"

# 3. 启动 OpenClaw（加载新配置）
openclaw gateway stop && openclaw gateway start

# 测试服务
curl -X POST http://localhost:8088/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
1 hidden lines
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
  }'

curl http://localhost:8088/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-7B",
    "messages": [{"role": "user", "content": "Read file /tmp/test.txt"}],
    "tools": [{"type": "function", "function": {"name": "read_file", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}}}}],
    "tools": [{"type": "function", "name": "read_file", "parameters": {"path": "/tmp/test.txt"}}],
    "tool_choice": "auto"
  }'