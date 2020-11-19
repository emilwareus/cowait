from .definition import TaskDefinition


def test_taskdef_serialization():
    sample = {
        'id':           'lazy-kcjvnrsg',
        'image':        'cowait/task:lazy',
        'name':         'lazy',
        'parent':       'root',
        'env':          {},
        'meta':         {},
        'inputs':       {},
        'ports':        {},
        'routes':       {},
        'volumes':      {},
        'storage':      {},
        'upstream':     None,
        'created_at':   '2020-02-02T20:00:02+00:00',
        'cpu':          None,
        'cpu_limit':    None,
        'memory':       None,
        'memory_limit': None,
        'owner':        'santa',
        "affinity" :    {}
    }

    taskdef = TaskDefinition.deserialize(sample)
    output = taskdef.serialize()
    assert sample == output


def test_taskdef_default_id():
    """
    Task definitions should be assigned an autogenerated ID if not provided.
    """
    taskdef = TaskDefinition(
        name='test',
        image='image',
    )
    assert isinstance(taskdef.id, str)


def test_taskdef_input_id():
    """ Task definitions can be passed an ID """
    taskdef = TaskDefinition(
        id='123',
        name='test',
        image='image',
    )
    assert taskdef.id == '123'
