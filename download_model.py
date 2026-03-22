# python3
# Create Date: 2026-03-21
# Author: Scc_hy
# Func: download TheBloke/Chinese-Llama-2-13B-GPTQ
# ==============================================================================

import os
from modelscope.hub.snapshot_download import snapshot_download


def download_model(model_name):
    out_dir = os.path.join(os.environ['SCC_DISK'], 'model_weight')
    print(f'{out_dir=}')
    model_id = os.path.join(out_dir, model_name)
    if not os.path.exists(model_id):
        snapshot_download(model_id=model_name, cache_dir=out_dir)

    print(f'Done: {model_name} -> LOCAL_DIR:{out_dir}')
    return None


if __name__ == '__main__':
    # 指定模型ID
    model_name = "TheBloke/Chinese-Llama-2-13B-GPTQ"
    model_name = "Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4"
    model_name = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"
    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct-AWQ" 
    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct-GPTQ-Int4"
    download_model(model_name)
