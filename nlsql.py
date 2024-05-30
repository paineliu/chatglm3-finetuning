
# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  #（保证程序cuda序号与实际cuda序号对应）
os.environ['CUDA_VISIBLE_DEVICES'] = "0"  #（代表仅使用第0，1号GPU）


from pathlib import Path
from typing import Annotated, Union

import typer
from peft import AutoPeftModelForCausalLM, PeftModelForCausalLM
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

ModelType = Union[PreTrainedModel, PeftModelForCausalLM]
TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

app = typer.Typer(pretty_exceptions_show_locals=False)


def _resolve_path(path: Union[str, Path]) -> Path:
    return Path(path).expanduser().resolve()


def load_model_and_tokenizer(model_dir: Union[str, Path]) -> tuple[ModelType, TokenizerType]:
    model_dir = _resolve_path(model_dir)
    if (model_dir / 'adapter_config.json').exists():
        model = AutoPeftModelForCausalLM.from_pretrained(
            model_dir, trust_remote_code=True, device_map='auto'
        )
        tokenizer_dir = model.peft_config['default'].base_model_name_or_path
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_dir, trust_remote_code=True, device_map='auto'
        )
        tokenizer_dir = model_dir
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_dir, trust_remote_code=True
    )
    return model, tokenizer

class NL2SQL():
    def __init__(self, model_dir):
        self.model, self.tokenizer = load_model_and_tokenizer(model_dir)

    def sql(self, request):
        respond = {}
        nl = request['text']
        prompt = "{}{}".format("""请你作为一个SQL终端，根据下面的数据库描述，只需要返回相应的SQL语句即可。下面是一个任务的指令，请写一个恰当的sql完成任务：
###指令：
知识数据库中有图片(picture)表、句子(ju)表、视频(video)表、等级(dengji)表、字(zi)表、音频(audio)表、混淆项(hunxiao)表、词句(ci_ju)表、词图(ci_picture)表、词音(ci_video)表、搭配(ci_dapei)表以及字搭配(zi_dapei)表。
图片(picture)表有如下列：id, 标签(tags), 意图标签(intention_tags), 路径(url), id是主键。
句子(ju)表有如下列：id, 句子(ju), md5(md5), 分词序列(ci), 词性标注序列(pos), 长度(len), 平均等级(avg_level), id是主键。
视频(video)表有如下列：id, 标签(tags), 意图标签(intention_tags), 路径(url), id是主键。
等级(dengji)表有如下列：id, 内容(term), 类型(type), 识读等级(shidu_level), 书写等级(shuxie_level), id是主键。
字(zi)表有如下列：id, 字(zi), 识读等级(shidu_level), 书写等级(shuxie_level), id是主键。
音频(audio)表有如下列：id, 标签(tags), 路径(url), id是主键。
混淆项(hunxiao)表有如下列：id, 内容(term), 拼音(term_pinyin), 词性(term_pos), 来源(source), 混淆项(hunxiao), 混淆项拼音(hunxiao_pinyin), 混淆项词性(hunxiao_pos), 类型(type), 频次(freq), 主键是id。
词句(ci_ju)表有如下列：词(ci), 句ID(r_id), ci是主键。
词图(ci_picture)表有如下列：词(ci), 图ID(r_id), ci是主键。
词音(ci_video)表有如下列：词(ci), 音频ID(r_id), ci是主键。
词搭配(ci_dapei)表有如下列：id, 词(ci), 搭配类型(dapei_type), 搭配(dapei), 频次(freq), id为主键。
字搭配(zi_dapei)表有如下列：id, 字(zi), 词(ci), 词等级(ci_level), 词频(ci_freq), id为主键。\n""", nl)
        
        response, _ = self.model.chat(self.tokenizer, prompt)
        respond['result'] = response
        return respond

    def bcc(self, request):
        respond = {}
        nl = request['text']
        prompt = "{}{}".format("请将下文解析成BCC检索式：\n", nl)
        
        response, _ = self.model.chat(self.tokenizer, prompt)
        respond['result'] = response
        return respond

    def chat(self, request):
        respond = {}
        nl = request['text']
        prompt = "{}{}".format("你的身份是汉语教师，请回答下述问题：\n", nl)
        
        response, _ = self.model.chat(self.tokenizer, prompt)
        respond['result'] = response
        return respond
    
if __name__ == "__main__":

    nlsql = NL2SQL('./output/sql_merge')
    query_json = {}
    query_json['text'] = '以字“掂”开头的字搭配的信息。'

    print(nlsql.sql(query_json))
