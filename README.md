# gloat-assignment

**Actions taken so far :**

1. Install the nmap >= 7.80 & ncrack >= 0.7 and build the tsunami-security-scanner app .
2. I dockerize the tsunami security scanner image , create a local one and build and run it ( create a container from this image).
3. I tagged it to the new tsuname image , commit and push it to the docker hub . so the new image name that I used its : **fadyabuhatoum/tsunami-security-scanner** .
4. I used helm charts , minikube , k8s and docker in order to create and check my local changes. 
5. I created a helm chart for unauthenticated-jupyter notebook in order to deploy 5 pods from these notebooks that already have vulnerabilities .
6. I created python file "main.py" which contains code that builds an unauthenticated-jupyter helm deployment dynamically and builds a tsunami pod for each jupyter pod and scans it. 

**Here are the instructions for running the whole deployment:**
1. Ensure that helm, minikube, docker, and kubectl are installed and working. 
2. Make sure that you have pip3 installed. 

The Script perform the following tasks: 
1. Create a helm chart deployment b running this command : " helm install unauthenticated-jupyter unauthenticated-jupyter/ --values unauthenticated-jupyter/values.yaml "
2. waiting for the pods to be in running status .
3. for each jupyter pod it create a tsunami pod and start to scan it by passing its IP as args . ( I add sleep(600) , because the average scanning will take **10 minutes** to scanning the pod ), so please make sure you will wait until the tsunami has finished scanning . 
4. create a new logs directories and files for each tsunami pod
5. Delete the helm and pods deployments by using (kubectl delete pods & helm delete unauthenticated-jupyter)

**In order to run it :**
1. Install the requirements libraries for pyhton . 

**# pip3 install -r requirements.txt**

2. Run the python script :

**# python3 main.py** 

**Also please read the comments in the main.py file . **

**Important**
If you want to keep the unauthenticated-jupyter and the tsunami pods running , you need to comment/delete these lines from main.py file : 
<img width="665" alt="image" src="https://user-images.githubusercontent.com/60876615/204044787-2f2d7572-a821-4c5c-b120-3c630120d9e8.png">
