from time import sleep
import os
import pandas as pd
import sys
import uuid

def container_exists(container):
    cmd = "sudo docker ps --format '{{.Names}}' | grep %s"%(container)
    list = os.popen(cmd).readlines()
    cmd2 = "sudo docker ps --format '{{.Names}}' | grep %s | wc -l"%(container)
    count =  os.popen(cmd2).read().strip()
    if int(count) >= 1:
        exists = True
    else:
        exists = False
    return (exists,list)

def create_container(container):
    cmd = "sudo docker run -v /doesnt/exist:/foo -w /foo -dit --name %s_%s python:3"%(container,str(uuid.uuid1()))
    os.popen(cmd)

if(str(sys.argv[1]) == '1'):
    predictions = pd.read_csv('/home/ubuntu/openwhisk/outputprediction/experiments/experiment_1_times.csv')
elif(str(sys.argv[1]) == '2'):
    predictions = pd.read_csv('/home/ubuntu/openwhisk/outputprediction/experiments/experiment_2_times.csv')
elif(str(sys.argv[1]) == '3'):
    predictions = pd.read_csv('/home/ubuntu/openwhisk/outputprediction/experiments/experiment_3_times.csv')
else:
    exit()

predictions = predictions['wait']
container = str(sys.argv[2])
for i in predictions:
    seconds = round(i*0.001,2) # Convert milliseconds to seconds for sleep method - 0.001 * time
    exists, list = container_exists(container)
    count = len(list)
    print(count)
    if not exists:
        create_container(container)
    sleep(seconds)

