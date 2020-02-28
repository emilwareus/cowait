
from typing import Any
from pipeline.network import Node
from pipeline.tasks import TaskDefinition, WORK, DONE, STOP, FAIL
from pipeline.tasks.messages import \
    TASK_INIT, TASK_LOG, TASK_STATUS, TASK_RETURN, TASK_FAIL


class WorkerAPI:
    """
    Upstream API client.
    """

    def __init__(self, node: Node, taskdef: TaskDefinition):
        self.taskdef = taskdef
        self.node = node
        self.id = taskdef.id

    async def msg(self, type: str, **msg) -> None:
        """
        Send a message upstream.

        Arguments:
            type (str): Message type
            kwargs (dict): Message fields
        """
        await self.node.parent.send({
            'id': self.id,
            'type': type,
            **msg,
        })

    async def init(self) -> None:
        """
        Send a task initialization message.

        Arguments:
            taskdef (TaskDefinition): New task definition
        """
        await self.msg(TASK_INIT, task=self.taskdef.serialize())

    async def run(self) -> None:
        """ Send status update: Running """
        await self.msg(TASK_STATUS, status=WORK)

    async def stop(self, id: str = None) -> None:
        """ Send status update: Stopped """
        id = self.id if id is None else id
        await self.msg(TASK_STATUS, status=STOP, id=id)
        await self.msg(TASK_RETURN, result={}, id=id)

    async def done(self, result: Any) -> None:
        """
        Send status update: Done, and return a result.

        Arguments:
            result (any): Any serializable data to return to the upstream task.
        """
        await self.msg(TASK_STATUS, status=DONE)
        await self.msg(TASK_RETURN, result=result)

    async def fail(self, error: str) -> None:
        """
        Send an error.

        Arguments:
            error (str): Error message
        """
        await self.msg(TASK_STATUS, status=FAIL)
        await self.msg(TASK_FAIL,   error=error)

    async def log(self, file: str, data: str) -> None:
        """
        Send captured log output.

        Arguments:
            file (str): Capture source (stdout/stderr)
            data (str): Captured output data
        """
        await self.msg(TASK_LOG, file=file, data=data)
