import multiprocessing
import sys
from io import StringIO
from multiprocessing import Process, Pipe
from pathlib import Path
import logging

from app.dependencies.path_manager import PathFactory
from app.models.test_model import TestResponse


class TestManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TestManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_inited"):
            self._inited = True

    def check_not_allowed_syscall(self) -> bool:
        # check not allowed syscall from src
        # TODO : some logic check not allowed syscall
        return False

    def execute_code_with_fork(self, test_id: int, src: str) -> TestResponse:
        # TODO : execute codes in container
        # TODO : handel err
        path_factory = PathFactory(test_id)
        recv_pipe, send_pipe = Pipe() # IPC not duplex PIPE
        process: Process = multiprocessing.Process(target=self.run_code, args=(src, send_pipe))
        process.start()
        process.join(5)  # wait for 5 seconds

        if process.is_alive():
            process.terminate()
            return TestResponse(is_right=False, test_id=test_id)

        if recv_pipe.poll():
            data = recv_pipe.recv()
        else:
            data = "None data"

        if not self.is_result_right(data, test_id):
            return TestResponse(is_right=False, test_id=test_id)

        return TestResponse(is_right=True, test_id=test_id, result=str(data))

    def run_test(self, test_id: int, src: str) -> TestResponse:
        return self.execute_code_with_fork(test_id, src)

    def is_result_right(self, result: str, test_id: int):
        # 데이터 아웃풋을 해당 test_id의 test_case와 비교
        # 각 객체를 string으로 직렬화해서 동등성 비교
        result_str = str(result)
        expected_output_path: Path = PathFactory(test_id).get_output_path()

        with open(expected_output_path,"r") as f:
            output_str = f.read()

        if result_str == output_str:
            return True

        return False


    def run_code(self, src: str,  send_pipe):
        try:
            code = src
            local_namespace = {}
            exec(code, {'__name__': '__main__'},local_namespace)
            result = local_namespace['solution']()
            send_pipe.send(result)
        except Exception as e:
            send_pipe.send(str(e))
        finally:
            send_pipe.close()


def get_test_manager() -> TestManager:
    return TestManager()
