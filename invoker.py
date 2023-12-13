from datetime import datetime
from time import sleep
import csv
import sys
import os
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
    sleep(2)
    guid = str(uuid.uuid1())
    name = container+'_'+guid
    cmd = "sudo docker run -v /doesnt/exist:/foo -w /foo -dit --name %s python:3"%(name)
    os.popen(cmd)
	print("CREATE CONTAINER")
    return name

def execute(container,function):
    try:
        cmd = "sudo docker cp %s %s:/foo/"%(function,container)
        os.popen(cmd)
        cmd2 = "sudo docker exec -i %s python %s"%(container,function)
        os.popen(cmd2)
        cmd3 = "sudo docker container kill %s"%(container)
        os.popen(cmd3)
        cmd4 = "sudo docker container rm %s"%(container)
        os.popen(cmd4)
		print("EXECUTE CONTAINER")
    except:
        type = "cold"
        name = create_container(container)
        execute(name,function)

def serverless_func(experiment,container,function):
    print('FUNCTION Start')
	start_time_obj = datetime.now()
    start_time = start_time_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    container = str(container)
    function = str(function)+".py"
    exists, list = container_exists(container)
    if exists:
        type = "warm"
        name = list[0].rstrip('\n')
    else:
        type = "cold"
        name = create_container(container) # Count = 0

    execute(name,function)

    end_time_obj = datetime.now()
    end_time = end_time_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    time_diff = end_time_obj - start_time_obj
    run_time = int(time_diff.total_seconds()*1000)

    if(str(experiment) == '1'):
        results = '/home/ubuntu/openwhisk/outputprediction/experiments/experiment_results.csv'
    elif(str(experiment) == '2'):
        results = '/home/ubuntu/openwhisk/outputprediction/experiments/experiment_results.csv'
    else:
        exit()

    with open(results, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([start_time, end_time, run_time, name, function, type])

serverless_func(sys.argv[1],sys.argv[2],sys.argv[3])
