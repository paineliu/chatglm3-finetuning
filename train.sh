#!/bin/bash
 
# 设置环境变量
export CUDA_VISIBLE_DEVICES=2
export NCCL_P2P_DISABLE="1"
export NCCL_IB_DISABLE="1"
 
# 执行 Python 脚本
# python finetune_hf.py  ./data/bcc/  ./model/ZhipuAI/chatglm3-6b  ./configs/lora_bcc.yaml
python finetune_hf.py  ./data/jss/  ./model/ZhipuAI/chatglm3-6b  ./configs/lora_jss.yaml
