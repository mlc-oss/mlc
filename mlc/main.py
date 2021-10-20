import docker


def main():
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        pass

    containers = client.containers.list()
    print(f'containers: {containers}')


if __name__ == "__main__":
    main()
