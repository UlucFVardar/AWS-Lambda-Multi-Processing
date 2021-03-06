# -*- coding: UTF-8 -*-

import requests
from layer_2_dataBase import DataBase as DB
from multiprocessing import Process
import boto3
import json
import time
import datetime

def invoke_layer_3(payload):
    invokeLam = boto3.client("lambda", region_name = "eu-central-1")
    resp = invokeLam.invoke(FunctionName="layer_3", InvocationType="Event", Payload = json.dumps(payload))


def main(event, context):
    time_number = event['delay']
    
    try:
        url = 'https://api.ipify.org/?format=json'
        r = requests.get(url)

        ip = json.loads(r.text)['ip']
        layer = event['layer']
        number = event['number']
        invoked_time = event['invoke_time']
    except:
        ip = 'null'
        layer = event['layer']
        number = event['number']
        invoked_time = event['invoke_time']

    db = DB('innodb')
    db.insert(ip,layer,number, invoked_time)

    for i in range(1,21):

        time.sleep(time_number)
        payload = {"number": (number*10)+i, "layer": layer + 1, 'delay': time_number, 'invoke_time':datetime.datetime.now() , 'test': event['test']}
        # create and run process
        p = Process(target=invoke_layer_3, args=(payload,))
        p.start()