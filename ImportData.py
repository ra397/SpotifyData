import json

with open('MyData/StreamingHistory1.json', 'r', encoding='utf-8') as f:
    streaming_data = json.load(f)
print(type(streaming_data))

