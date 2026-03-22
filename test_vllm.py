# 测试是否能加载（不启动服务）

import os 
from vllm import LLM, SamplingParams


# model_name = 'Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4'
# llm = LLM(
#     model=os.path.join(os.environ['SCC_DISK'], 'model_weight', model_name),
#     quantization='gptq_marlin',  # 使用 gptq_marlin 加速
#     dtype='float16',
#     max_model_len=2048,  # 从 4096 降低到 2048
#     gpu_memory_utilization=0.95,  # 从 0.90 提高到 0.95
#     trust_remote_code=True,
#     enforce_eager=True
# )
model_name = 'Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4'
llm = LLM(
    model=os.path.join(os.environ['SCC_DISK'], 'model_weight', model_name),
    quantization='gptq_marlin',  # 使用 gptq_marlin 加速
    dtype='float16',
    max_model_len=16384,  # 从 4096 降低到 2048
    gpu_memory_utilization=0.88,  # 从 0.90 提高到 0.95
    trust_remote_code=True,
    enforce_eager=True
)

print("✅ 模型加载成功")

# 简单测试
prompts = ["你好"]
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)
outputs = llm.generate(prompts, sampling_params)
print(outputs[0].outputs[0].text)

print('✅ 模型加载成功，显存充足')
