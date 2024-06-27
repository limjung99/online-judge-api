import multiprocessing
import os
import subprocess
import sys
from multiprocessing import process, Process
from pathlib import Path

from models.test_model import TestResponse


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

    def execute_code_in_container(self, test_id: int) -> TestResponse:
        # execute code in container
        src_file = Path(f"~/projects/code-judge-server/app/resources/code/{test_id}.py")
        err_file = Path(f"~/projects/code-judge-server/app/resources/error/{test_id}.txt")
        input_file = Path(f"~/projects/code-judge-server/app/resources/input/input{test_id}.txt")

        # output_file = f"resources/output/output{test_id}.txt"

        # clojure
        def run_code():
            try:
                with open(src_file, "r") as sf:
                    code = sf.read()
                    exec(code)
            except Exception as e:
                with open(err_file, "w") as errf:
                    errf.write(str(e))

        process: Process = multiprocessing.Process(target=run_code)
        process.start()
        process.join(5)  # wait for 5 seconds

        if process.is_alive():
            process.terminate()
            return TestResponse(is_right=False, test_id=test_id)

        return TestResponse(is_right=True, test_id=test_id)

    def run_test(self, test_id: int) -> TestResponse:
        return self.execute_code_in_container(test_id)


def get_test_manager() -> TestManager:
    return TestManager()
