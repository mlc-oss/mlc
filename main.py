import docker


def main():
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        pass

    containers = client.containers.list()
    print(f'containers: {containers}')

    images = client.images.list()
    print(f'images: {images}')

    image = client.images.get('nvcr.io/nvidia/pytorch:21.09-py3')
    print(f'image: {image}')

    container = client.containers.run(image, command=None, detach=True)
    print(f'container: {container}')
    container.logs()
    # container.kill()
    container.stop()
    container.remove()


if __name__ == "__main__":
    main()
