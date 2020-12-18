from flask import Flask,request,jsonify
from docker_api import *

app = Flask(__name__)



@app.route("/")
def index():
    return "Docker Api  in Flask"

@app.route("/images")
def list_images():
    return jsonify({"images":json.loads(docker_images())})


@app.route("/containers")
def list_containers():
    return jsonify({"containers": json.loads(docker_ps())})


@app.route("/container/stats")
def container_stats():
    return jsonify({"stats":json.loads(docker_stats())})


@app.route("/container/run")
def run_container():

    args = request.args
    con_name = request.args.get("name")
    image_name = request.args.get("image")
    version = 'latest' if request.args.get("version",'')=='' else args.get("version")
    return jsonify({"conatiner":json.loads(docker_run(con_name,image_name,version=version))})

@app.route("/networks")
def container_networks():
    return jsonify({"networks":json.loads(docker_network_ls())})


@app.route("/network/create")
def container_network_create():
    args = request.args
    net_name = args.get("name")
    driver_name = 'bridge' if args.get("driver_name",'')=='' else args.get("driver_name")
    return jsonify({"network": json.loads(docker_network_create(name=net_name,driver_name=driver_name))})



@app.route("/volumes")
def container_volumes():
    return jsonify({"volumes":json.loads(docker_volume_ls())})


@app.route("/volume/create")
def container_volume_create():
    args = request.args
    vol_name = args.get("name")
    driver_name = 'local' if args.get("driver_name",'')=='' else args.get("driver_name")
    return jsonify({"volume":json.loads(docker_volume_create(name=vol_name,driver_name=driver_name))})



@app.route("/image/search")
def image_search():
    args = request.args
    return jsonify({"Docker Hub images results":json.loads(docker_search(args.get("name",'')))})

@app.route("/container/stop")
def container_stop():
    args = request.args
    con_name = request.args.get("name")
    return jsonify({"stopped container":json.loads(docker_stop(con_name))})


@app.route("/container/remove")
def container_remove():
    args = request.args
    con_name = request.args.get("name")
    return jsonify({"removed container": json.loads(docker_remove(con_name))})


@app.route("/container/remove/all")
def container_remove_all():
    return jsonify({"removed containers": json.loads(docker_remove_all())})






if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
