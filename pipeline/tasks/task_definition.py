from __future__ import annotations
from marshmallow import Schema, fields, post_load
from ..utils import uuid


class TaskDefinition(object):
    """
    Defines a Task :)

    Attributes:
        name (str): Task import name.
        image (str): Task image.
        id (str): Task id. If None, an id will be autogenerated.
        parent (str): Parent connection string. Defaults to None.
        namespace (str): Task namespace.
        config (dict): Configuration values
        inputs (dict): Input values
        meta (dict): Freeform metadata
        env (dict): Environment variables
    """

    def __init__(self, 
        name:      str, 
        image:     str, 
        id:        str  = None, 
        parent:    str  = None,
        namespace: str  = 'default', 
        config:    dict = { }, 
        inputs:    dict = { }, 
        meta:      dict = { },
        env:       dict = { },
    ):
        """
        Arguments:
            name (str): Task import name.
            image (str): Task image.
            id (str): Task id. If None, an id will be autogenerated.
            parent (str): Parent connection string. Defaults to None.
            namespace (str): Task namespace.
            config (dict): Configuration values
            inputs (dict): Input values
            meta (dict): Freeform metadata
            env (dict): Environment variables
        """
        self.id        = '%s-%s' % (name, uuid()) if not id else id
        self.name      = name
        self.image     = image
        self.parent    = parent
        self.namespace = namespace
        self.config    = config
        self.inputs    = inputs
        self.meta      = meta
        self.env       = env


    def serialize(self) -> dict:
        """ Serialize task definition to a dict """
        return TaskDefinitionSchema().dump(self)


    @staticmethod
    def deserialize(taskdef: dict) -> TaskDefinition:
        """ Deserialize task definition from a dict """
        return TaskDefinitionSchema().load(taskdef)



class TaskDefinitionSchema(Schema):
    """ TaskDefinition serialization schema. """

    id        = fields.Str(required=True)
    name      = fields.Str(required=True)
    image     = fields.Str(required=True)
    parent    = fields.Str(allow_none=True)
    namespace = fields.Str(missing='default')
    config    = fields.Dict(missing={})
    inputs    = fields.Dict(missing={})
    meta      = fields.Dict(missing={})
    env       = fields.Dict(missing={})

    @post_load
    def make_taskdef(self, data: dict, **kwargs) -> TaskDefinition:
        return TaskDefinition(**data)
