
import requests
from requests.auth import HTTPDigestAuth


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

# Query the API for all the snapshots for the chosen cluster
sr = requests.get(f"{endpoint}/snapshots", auth=my_auth).json()

## Init choice variable
snapshot_choice = -1
if len(sr["results"]) == 1:
    snapshot_choice = 0
    
## Otherwise let the user choose which snapshot
else:
    ## Loop through and display each snapshot along with it's index
    for idx, result in enumerate(sr["results"]):
        ## Not all snapshots have a description, so display description conditionally
        if "description" in result.keys():
            print(f"[{idx}] {result['createdAt']} {result['description']}")
        else:
            print(f"[{idx}] {result['createdAt']}")    
        
    ## Record which cluster the user chooses
    snapshot_choice = int(input("Select a snapshot: "))
    
## Get ID for chosen project
snapshot_id = sr["results"][snapshot_choice]["id"]

# Restore from chosen snapshot
## Init required body parameters for posting to the restoreJobs endpoint
body = {
    "deliveryType": "automated",
    "snapshotId": str(snapshot_id),
    "targetClusterName": str(cluster_name),
    "targetGroupId": str(project_id)
}
## Begin the restoreJob
rr = requests.post(f"{endpoint}/restoreJobs", auth=my_auth, json=body)