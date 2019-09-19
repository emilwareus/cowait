import os.path
from .task_image import TaskImage
from ..engine import get_cluster_provider
from ..tasks import TaskDefinition


def build(task: str) -> TaskImage:
    image = TaskImage.create(task)
    print('context path:', image.root)

    # find task-specific requirements.txt
    # if it exists, it will be copied to the container, and installed
    requirements = image.find_file_rel('requirements.txt')
    if requirements:
        print('found custom requirements.txt:', requirements)

    # find custom Dockerfile
    # if it exists, build it, then extend that instead of the default base image
    dockerfile = image.find_file('Dockerfile')
    if dockerfile:
        print('found custom Dockerfile:', os.path.relpath(dockerfile, image.root))
        print('building custom base image...')
        logs = image.build_custom_base(dockerfile)
        for log in logs:
            if 'stream' in log:
                print(log['stream'], flush=True, end='')
    
    print('building task image...')
    logs = image.build(
        requirements=requirements,
    )

    for log in logs:
        if 'stream' in log:
            print(log['stream'], flush=True, end='')

    return image


def run(task: str, provider: str, inputs: dict = { }, config: dict = { }, env: dict = { }):
    task_image = f'johanhenriksson/pipeline-task:{task}'

    # grab cluster provider
    cluster = get_cluster_provider(type=provider)
    
    # run task
    taskdef = TaskDefinition(
        name      = task,
        image     = task_image,
        config    = config,
        inputs    = inputs,
        env       = env,
        namespace = 'default',
    )
    task = cluster.spawn(taskdef)

    # capture & print logs
    logs = cluster.logs(task)
    print('-- TASK OUTPUT: -------------------------------------')
    for log in logs:
        print(log, flush=True)
    print('-----------------------------------------------------')


def push(task: str) -> TaskImage:
    image = build(task)

    print('pushing...')
    logs = image.push('johanhenriksson/pipeline-task')
    for _ in logs:
        pass

    print('done')
    return image
