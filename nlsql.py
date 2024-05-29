
# -*- coding:utf-8 -*-
import os
import time
import jwt
import secrets
from time import sleep
import requests
import json

from pathlib import Path
from typing import Annotated, Union

import typer
import json
from peft import AutoPeftModelForCausalLM, PeftModelForCausalLM

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)
from datetime import datetime, timedelta, timezone
    
def get_res(interface, text):
    
    rets = []
    query_json = {}
    query_json['text'] = text
    query_json['total'] = 3
    resources = jss_post('202.112.194.54', '8100', interface, json.dumps(query_json))
    resources = json.loads(resources)
    for res in resources['data']:
        rets.append([{'id':'', 'type':interface.split('_')[1], 'value':'https://static.blcu.edu.cn' + res['url']}])
    return rets


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


class NLSQL():
    def __init__(self):
        model, tokenizer = load_model_and_tokenizer(model_dir)
    
        pass
    
    def chat(self, request):
        respond = {}
        respond['code'] = 200
        respond['message'] = 'ok'
        respond['data'] = {}
        respond['data']['result'] = request['messages'][-1]
        respond['data']['resources'] = {}
        respond['data']['resources']['video'] = get_res('search_video', request['messages'][-1]['content'])
        respond['data']['resources']['picture'] = get_res('search_picture', request['messages'][-1]['content'])
        respond['data']['resources']['audio'] = get_res('search_audio', request['messages'][-1]['content'])
        respond['data']['resources']['text'] = []#get_res('search_dapei', request['messages'][-1]['content'])
        respond['data']['resources']['quiz'] = []

        respond['data']['result']['role'] = 'assistant'
        respond['data']['result']['content'] = '为您找到以下资源：'
        return respond
        
    def addAnswers(self, request):
        token = request['token']
        if (self.is_valid_token(token)):
            return {}
        return {}
    
    def addReviews(self, request):
        token = request['token']
        if (self.is_valid_token(token)):
            return {}
        return {}

if __name__ == "__main__":

    nlsql = NLSQL()
    query_json = {}
    query_json['messages'] = [{'content':'北京的图片','role':'user'}]

    print(nlsql.chat(query_json))
