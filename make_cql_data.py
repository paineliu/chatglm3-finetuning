import json
import pandas as pd
f = open("./cql-annotated/simple.txt", encoding="utf-8")
train_data = []
test_data = []
val_data = []

line_total = 0
for each in f:
    items = each.strip().split('\t')
    if len(items) == 2:
        cql = items[0]
        nl = items[1]
        if '#' in nl:
            nl  = nl.split('#')[0]
        	
        data ={
		    "conversations": [
                {"role": "user",
                "content": "{}{}".format("请将下文解析成CQL语句：\n", nl)
                    }, 
                {"role": "assistant", 
                    "content": "{}".format(cql)
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

f = open("./data/train.json",'w',encoding='utf-8')
for each in train_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()

f = open("./data/test.json",'w',encoding='utf-8')
for each in test_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()

f = open("./data/dev.json",'w',encoding='utf-8')
for each in val_data:
    item = json.dumps(each, ensure_ascii=False)
    f.write("{}\n".format(item))
f.close()