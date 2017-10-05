import wolframalpha
import urllib
from xml.etree import ElementTree as etree
import sys


# your wolfram alpha app id
app_id = '8KHGJP-YYasdfasdf'
client = wolframalpha.Client(app_id)

question = 'Why is the sky blue?'
res = client.query(question)

bool = 0
x = 0

for pod in res.pods:
    if pod.primary or pod.title == 'Result':
        bool = 1
        # create a pod to use later
        results = wolframalpha.Pod(pod)

output = ''
if bool:
    #response = response + (res.results).text
    output = (results).text
else:
    for pod in res.pods:
        for sub in pod.subpods:
            output = output + sub.text
print(output)

