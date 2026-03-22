

import os 
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8088/v1", api_key="sk-test")
# model_name = os.path.join(os.environ['SCC_DISK'], 'model_weight', "Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4")
model_name = 'qwen2.5-7B'
print(model_name)
try:
    # 简单对话测试
    resp = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": "你好"}],
        max_tokens=100
    )
    print("✅ 连接成功")
    print(f"回复: {resp.choices[0].message.content}")
    print(f"用量: {resp.usage.total_tokens} tokens")
    
    # 流式测试
    print("\n流式测试:")
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": "1+1=?"}],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n流式测试-CoT:")
    cot = """
请一步一步思考并解答这道题。在得出最终答案前，先解释你的推理过程。
题目：小明有 24 颗糖，给了小红 1/3，又给了小刚剩下的一半，最后还剩多少颗？
思考过程：/think
    """
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": cot}],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n流式测试-few_shot:")
    few_shot = """
请按步骤解答数学题：

【示例1】
题目：小明有 10 个苹果，吃掉 3 个，又买了 5 个，现在有几个？
解答：
1. 原有 10 个
2. 吃掉 3 个：10 - 3 = 7 个
3. 又买 5 个：7 + 5 = 12 个
答案：12 个

【示例2】
题目：一本书 120 页，第一天看 1/4，第二天看剩下的 1/3，还剩多少页？
解答：
1. 总页数 120 页
2. 第一天看：120 × 1/4 = 30 页，剩 90 页
3. 第二天看：90 × 1/3 = 30 页，剩 60 页
答案：60 页

【待解答】
题目：小明有 24 颗糖，给了小红 1/3，又给了小刚剩下的一半，最后还剩多少颗？
解答：/no_think
    """
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": few_shot}],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)


except Exception as e:
    print(f"❌ 错误: {e}")