
# -*- coding:utf-8 -*-
import os
import time
from typing import Union, List
from typing import Optional
import uvicorn
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from chatedu_engine import ChatEdu

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='jss lang-elem server')
    parser.add_argument('-m', '--message', type=int, default=1, required=False, help='output debug message')
    parser.add_argument('-p', '--port', type=int, default=8102, required=False, help='port number')
    parser.add_argument('-w', '--workers', type=int, default=1, required=False, help='worker number')

    return parser.parse_args()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load resources
    global g_chatEdu
    print('liftspan', 'start...')
    args = parse_args()
    g_chatEdu = ChatEdu()
    print('liftspan', 'finish.')
    yield
    # Clean up and release resources
    pass

app = FastAPI(lifespan=lifespan)
      
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"The parameter is incorrect. {request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})

class MessageItem(BaseModel):
    role:str
    content:str

class RespondItemModel(BaseModel):
    index: int
    message: MessageItem
    finish_reason: str = "stop"

class LessonInfo(BaseModel):
    book_name:str
    lesson_type:str
    lesson_level:str
    
class ExamInfo(BaseModel):
    exam_type:str
    exam_level:str
    
class ChatContext(BaseModel):
    user_id:str
    lessonInfo:LessonInfo = None
    examInfo:ExamInfo = None
    quiz:str
    focus_item:str

class ChatModel(BaseModel):
    modal: str = ''
    token: str
    context:ChatContext = None
    messages:list[MessageItem]
    n: int = 5
    top_p: float = 1.0
    stream: bool = False

class TokenModel(BaseModel):
    userName: str = ''

class UsageModel(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ResondData(BaseModel):
    id: str = "chatcmpl-123"
    obj: str = "chat.completion"
    created: int = 1677652288
    result: MessageItem
    choices: List[RespondItemModel]
    usage: UsageModel

class RespondModel(BaseModel):
    code:int = 0
    message:str = "OK"
    data:ResondData

class AnswerItem(BaseModel):
    type:str
    val:str

class RecordItem(BaseModel):
    begin:str
    end:str
    operator:str
    item_id:str
    answer:str

class AnswerMode(BaseModel):
    exam_id:str
    student_id:str
    begin_time:str
    finish_time:str
    items:List[AnswerItem]
    record:List[RecordItem]

    
@app.post("/getToken")
async def getToken(tokenModel: TokenModel):    
    print('{} {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), tokenModel.model_dump()))
    start = time.time()
    respond = g_chatEdu.getToken(tokenModel.model_dump())
    end = time.time()

    return respond


@app.post("/chat")
async def exam_chat(charRequestModel: ChatModel):    
    print('{} {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), charRequestModel.model_dump()))
    start = time.time()
    respond = g_chatEdu.chat(charRequestModel.model_dump())
    end = time.time()

    return respond


if __name__ == "__main__":
    args = parse_args()
    print('chatedu_fastapi server', 'port = {}, worker = {}.'.format(args.port, args.workers))
    uvicorn.run(app='chatedu_fastapi:app', host='0.0.0.0', log_level='warning', port=args.port, workers=args.workers, reload=False)
