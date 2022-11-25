from kubernetes import client, config
import subprocess
import os
import time
import random


# First of all run the helm chart in order to create unauthenticated-jupyter deployment which have 5 pods
subprocess.run(["helm", "install", "unauthenticated-jupyter", "unauthenticated-jupyter/", "--values=unauthenticated-jupyter/values.yaml"])

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()

# Waiting for full creation of helm chart 
time.sleep(30)

print("Listing pods with their IPs:")
list_pods = v1.list_pod_for_all_namespaces(watch=False)
counter = 0 
for i in list_pods.items:
    if 'unauthenticated-jupyter' in i.metadata.name:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        
        # Create a new tsunami-security-scanner pod for each unauthenticated-jupyter pod in order to scan it .
        subprocess.run(["kubectl", "run", f"tsunami-{counter}", " --restart='OnFailure'",
                        "--image=fadyabuhatoum/tsunami-security-scanner:latest",
                        " --", f" --ip-v4-target='{i.status.pod_ip}' "])
        counter+=1


# time sleep for 10 minutes - ( average tsunami security full scan take 10 minutes)
print("Sleep for 10 minutes in order to ")
time.sleep(600)

list_new_created_pods = v1.list_pod_for_all_namespaces(watch=False)
# Parent Directory path
parent_dir = "../gloat-assignment/"
for pod in list_new_created_pods.items:
    if 'tsunami-' in pod.metadata.name:
        print("%s\t%s\t%s" % (pod.status.pod_ip, pod.metadata.namespace, pod.metadata.name))
        # Save the logs

        # Directory
        directory = f"logs-{pod.metadata.name}"

        # Path
        path = os.path.join(parent_dir, directory)

        # make directory
        os.mkdir(path)
        print("Directory '%s' created" % directory)

        # get the pod logs and pods directories and files
        scanning_logs_per_pod = subprocess.check_output(['kubectl', 'logs', f'{pod.metadata.name}'])
        result = subprocess.check_output(['ls', '-l'])

        # write a new logs file .
        with open(f'{path}/logs.txt', 'w') as f:
            f.write(f'{result}')
            f.write(f'{scanning_logs_per_pod}')

# Sleep before delete the tsunami scanner pods 
time.sleep(30)
print("Now we need to delete our tsunami scanner pods")
for pod in list_new_created_pods.items:
    if 'tsunami-' in pod.metadata.name:
        subprocess.run(['kubectl','delete' ,'pod', f'{pod.metadata.name}'])


# delete the helm chart 
print("Delete unauthenticated-jupyter helm deployment")
subprocess.run(['helm','delete' ,'unauthenticated-jupyter'])



