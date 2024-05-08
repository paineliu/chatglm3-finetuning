#!/bin/bash
 
# 设置环境变量
export CUDA_VISIBLE_DEVICES=2
export NCCL_P2P_DISABLE="1"
export NCCL_IB_DISABLE="1"
 
# 执行 Python 脚本

python inference_hf.py output/checkpoint-3000 --prompt "请将下文解析成CQL语句：\n查找以动词\"介绍\"开头，后面跟有8个任意词，然后是一个普通名词的语句。"