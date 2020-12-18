import subprocess as sp
import json


# a class to represent the Docker instance or container
class Docker:
    
    total_containers = []

    def __init__(self,container_id,image_name,command,created,status,name,ports=''):
        self.container_id = container_id
        self.image_name = image_name
        self.command = command
        self.created = created
        self.satus = status
        self.ports = ports
        self.name = name

    def __repr__(self):
        return self.name
    
    @classmethod
    def list_docker(cls):
        temp_total_containers = []
        args = [list(filter(lambda x: x!='',con.split("  "))) for con in json.loads(run_cmd("docker ps"))["output"].split("\n")[1:]] 
        print(args)
        for con_details in args:
            temp_total_containers.append(cls(*con_details))
        cls.total_containers = list(set(temp_total_containers))
        return cls.total_containers


# actual methods start from here



# helper function to run the command and give the output in json format"
def run_cmd(cmd):
    
    status,output = sp.getstatusoutput(cmd)
    response = { "status": status , "output": output}
    return json.dumps(response,indent=3)




# similar to docker run

def docker_run(container_name,image_name,version="latest"):
    cmd = f'docker run -dit --name {container_name} {image_name}:{version}'

    return run_cmd(cmd) 




# similar to docker ps

def docker_ps():
    cmd = 'docker ps -a'
    docker_container_properties =["CONTAINER ID","IMAGE","COMMAND","CREATED","STATUS","PORTS ","NAMES"]
    docker_containers_list =[]
    for con_prop_value in json.loads(run_cmd(cmd))["output"].split("\n")[1:]:
        con_prop_values = [i.strip() for i in con_prop_value.split("    ") if i!='']
        docker_containers_dict={prop:value for prop,value in zip(docker_container_properties,con_prop_values)}
        docker_containers_list.append(docker_containers_dict)
    
    return(json.dumps(docker_containers_list,indent=3))



# similar to docker images

def docker_images():
    cmd = "docker images"
    docker_images_properties=["REPOSITORY","TAG","IMAGE ID","CREATED","SIZE"]
    docker_images_list=[]
    for img_prop_value in json.loads(run_cmd(cmd))["output"].split("\n")[1:]:
        img_prop_values = [i.strip() for i in img_prop_value.split("  ") if i!='']
        docker_images_dict={prop:value for prop,value in zip(docker_images_properties,img_prop_values)}
        docker_images_list.append(docker_images_dict)
    return json.dumps(docker_images_list,indent=3)



# similar to docker stats

def docker_stats():
    cmd = 'docker stats --no-stream'
    docker_container_properties =["CONTAINER ID","NAME","CPU %","MEM USAGE / LIMIT","MEM %","NET I/O","BLOCK I/O","PIDS"]
    docker_containers_list =[]
    for con_prop_value in json.loads(run_cmd(cmd))["output"].split("\n")[1:]:
        con_prop_values = [i.strip() for i in con_prop_value.split("  ") if i!='']
        docker_containers_dict={prop:value for prop,value in zip(docker_container_properties,con_prop_values)}
        docker_containers_list.append(docker_containers_dict)

    return(json.dumps(docker_containers_list,indent=3))



# list docker network 

def docker_network_ls():
    cmd = "docker network ls"
    docker_network_properties = [ "NETWORK ID","NAME","DRIVER","SCOPE"]

    docker_networks_list= []

    for net_prop_value in json.loads(run_cmd(cmd))["output"].split("\n")[1:]:
        net_prop_values = [i.strip() for i in net_prop_value.split("  ") if i!='']
        docker_networks_dict={prop:value for prop,value in zip(docker_network_properties,net_prop_values)}
        docker_networks_list.append(docker_networks_dict)

    return(json.dumps(docker_networks_list,indent=3))



# docker network create

def docker_network_create(name,driver_name="bridge"):
    cmd = f'docker network create { name } -d { driver_name }'
    return run_cmd(cmd)



# docker volumes

def docker_volume_ls():
    cmd ='docker volume ls'
    docker_volume_properties = ["DRIVER","VOLUME NAME"]

    docker_volumes_list =[]
    for vol_prop_value in json.loads(run_cmd(cmd))["output"].split("\n")[1:]:
        vol_prop_values = [i.strip() for i in vol_prop_value.split("  ") if i!='']
        docker_volumes_dict={prop:value for prop,value in zip(docker_volume_properties,vol_prop_values)}
        docker_volumes_list.append(docker_volumes_dict)

    return(json.dumps(docker_volumes_list,indent=3))



# create docker volume

def docker_volume_create(name,driver_name="local"):
    cmd = f'docker volume create --name { name } -d { driver_name }'
    return run_cmd(cmd)




# search for the images

def docker_search(query):
    cmd = f'docker search { query }'

    dockerhub_search_properties= ["NAME","DESCRIPTION","STARS","OFFICIAL","AUTOMATED"]

    docker_search_result_list = []

    for result_prop_value in json.loads(run_cmd(cmd))["output"].split("\n")[1:]:
        result_prop_values = [i.strip() for i in result_prop_value.split("  ") if i!='']
        docker_search_results_dict={prop:value for prop,value in zip(dockerhub_search_properties,result_prop_values)}
        docker_search_result_list.append(docker_search_results_dict)

    return(json.dumps(docker_search_result_list,indent=3))



# docker stop container
def docker_stop(name):
    cmd = f'docker stop {name}'
    return run_cmd(cmd)



# docker remove container
def docker_remove(name):
    cmd = f'docker rm -f {name}'
    return run_cmd(cmd)



# docker remove all containers
def docker_remove_all():
    cmd = 'docker rm -f $(docker ps -aq)'
    return run_cmd(cmd)

