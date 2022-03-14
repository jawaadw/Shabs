import time
import requests
from requests.auth import HTTPDigestAuth

# Initial api endpoint
endpoint = "https://cloud.mongodb.com/api/atlas/v1.0/groups"

# Auth
public_key =  ""
private_key = ""
my_auth = HTTPDigestAuth(public_key, private_key)

# Query the API for all projects
pr = requests.get(endpoint, auth=my_auth).json()

## Init choice variable
project_choice = -1
## Default to 0 if there is only one project
if (len(pr["results"]) == 1):
    project_choice = 0

## Otherwise let the user choose which project 
else:
    ## Loop through and display each project along with it's index
    for idx, result in enumerate(pr["results"]):
        print(f"[{idx}] {result['name']}")
        
    ## Record which project the user chooses
    project_choice = int(input("Select a project: "))

## Get ID for chosen project
project_id = pr["results"][project_choice]["id"]
## Update the endpoint with the project id
endpoint += f"/{project_id}/clusters"

# Query the API for all the cluster names for the chosen project
cr = requests.get(endpoint, auth=my_auth).json()

## Init choice variable
cluster_choice = -1
## Default to 0 if there is only one cluster
if (len(cr["results"]) == 1):
    cluster_choice = 0

## Otherwise let the user choose which cluster
else:
    ## Loop through and display each cluster along with it's index
    for idx, result in enumerate(cr["results"]):
        print(f"[{idx}] {result['name']}")
        
    ## Record which cluster the user chooses
    cluster_choice = int(input("Select a cluster: "))
    
## Get the name for the chosen project
cluster_name = cr["results"][cluster_choice]["name"]
## Update the endpoint with the cluster name
endpoint += f"/{cluster_name}/backup"

# Take a snapshot of the cluster
## Init required body parameters for posting to the snapshots endpoint
body = {
    "description": "Snapshot taken from script",
    "retentionInDays": 7,
}
## Begin taking a snapshot
sr = requests.post(f"{endpoint}/snapshots", auth=my_auth, json=body).json()
## Record the newly created snapshot's id
snapshot_id = sr["id"]

# Check if the snapshot is completed
# Sleep for 5 minutes if not
completed = False
while not completed:
    ## Get all snapshots
    sr2 = requests.get(f"{endpoint}/snapshots", auth=my_auth, json=body).json()
    ## For each snapshot...
    for result in sr2["results"]:
        
        ## If this snapshot matches the one we just took...
        if result["id"] == snapshot_id:
            
            ## If it's status is completed...
            if result["status"] == "completed":
                ## Set the completed variable to True and break the for loop
                completed = True
                break
            
            ## Otherwise sleep for 5 minutes and break the for loop
            else:
                time.sleep(30)
                break
            
    ## If the snapshot status is completed, break the while loop
    if completed:
        break

# Restore using the snapshot which was just taken
## Init required body parameters for posting to the restoreJobs endpoint
body = {
    "deliveryType": "automated",
    "snapshotId": str(snapshot_id),
    "targetClusterName": str(cluster_name),
    "targetGroupId": str(project_id)
}
## Begin the restoreJob
rr = requests.post(f"{endpoint}/restoreJobs", auth=my_auth, json=body)