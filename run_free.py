import docker
import argparse

def start_docker_containers(start_port=18080):
    client = docker.from_env()

    # Check if there are any containers running with the specified image
    running_containers = client.containers.list(filters={"ancestor": "shoaphil/free-mind"})

    if len(running_containers) == 0:
        # If no containers are running, start two new containers with consecutive ports
        port_range = range(start_port, start_port + 2)
    else:
        if start_port != 18080:
            # If a starting port is provided, use it to define the port range for the new containers
            port_range = range(start_port, start_port + 2)
        else:
            # If no starting port is provided, find the highest port number and increment it by 1
            max_port = max(int(c.attrs["HostConfig"]["PortBindings"]["8080/tcp"][0]["HostPort"]) for c in running_containers)
            port_range = range(max_port + 1, max_port + 3)

        # Stop and remove the existing containers
        for c in running_containers:
            c.remove(force=True)
            print(f"Container {c.short_id} removed.")

    # Start two new containers with the specified image and ports
    new_ports=[]
    for i, port in enumerate(port_range):
        container = client.containers.run("shoaphil/free-mind", detach=True, ports={"8080/tcp": port})
        print(f"Container {container.short_id} started on port {port}.")
        new_ports.append(port)
    return new_ports

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-port", type=int, default=18080, help="Starting port number")
    args = parser.parse_args()

    start_docker_containers(start_port=args.start_port)

