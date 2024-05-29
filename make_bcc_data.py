import json
import pandas as pd
f = open("./data/bcc8_dataset.jsonl", encoding="utf-8")
train_data = []
test_data = []
val_data = []

line_total = 0
for each in f:
    items = json.loads(each)
    bcc = items['bcc']
    nl = items['meaning']
    if '#' in nl:
        nl  = nl.split('#')[0]
    data ={
        "conversations": [
            {"role": "user",
            "content": "{}{}".format("请将下文解析成BCC检索式：\n", nl[3:])
                }, 
            {"role": "assistant", 
                "content": "{}".format(bcc)
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

f = open("./data/bcc_train.json",'w',encoding='utf-8')
for each in train_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()

f = open("./data/bcc_test.json",'w',encoding='utf-8')
for each in test_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()

f = open("./data/bcc_dev.json",'w',encoding='utf-8')
for each in val_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()