import json
import pandas as pd
f = open("./data/jss/kb_dataset4.json", encoding="utf-8")
train_data = []
test_data = []
val_data = []

line_total = 0
for each in f:
    items = json.loads(each)
    prompt = items['prompts']
    keywords = items['keywords']
        
    data ={
        "conversations": [
                {
                    "role": "user",
                    "content": "{}{}".format("请提取下文考点和意图：\n", prompt)
                }, 
                {
                    "role": "assistant", 
                    "content": "考点：{}\n意图：{}".format(keywords[0], keywords[1])
                }
            ]
        }
    if (line_total % 10) < 8:
        train_data.append(data)
    elif (line_total % 10) < 9:
        test_data.append(data)
    else:
        val_data.append(data)
    line_total += 1    

f = open("./data/jss/train.json",'w',encoding='utf-8')
for each in train_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()

f = open("./data/jss/test.json",'w',encoding='utf-8')
for each in test_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()

f = open("./data/jss/dev.json",'w',encoding='utf-8')
for each in val_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()