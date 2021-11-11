import docker

import mlc.interops


def main():
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        pass

    containers = client.containers.list()
    print(f'containers: {containers}')

    images = client.images.get('nvcr.io/nvidia/pytorch:21.09-py3')
    print(f'images: {images}')


if __name__ == "__main__":
    main()
