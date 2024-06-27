import multiprocessing
from multiprocessing import Process
from pathlib import Path

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

    def execute_code_with_fork(self, test_id: int) -> TestResponse:
        # execute codes in container
        src_file = Path(f"app/resources/codes/{test_id}.py")
        err_file = Path(f"app/resources/error/{test_id}.txt")
        input_file = Path(f"app/resources/inputs/input{test_id}.txt")
        output_file = Path(f"app/resources/outputs/output{test_id}.txt")

        process: Process = multiprocessing.Process(target=self.run_code, args=(src_file, err_file))
        process.start()
        process.join(5)  # wait for 5 seconds

        if process.is_alive():
            process.terminate()
            return TestResponse(is_right=False, test_id=test_id)

        return TestResponse(is_right=True, test_id=test_id)

    def run_test(self, test_id: int) -> TestResponse:
        return self.execute_code_with_fork(test_id)

    def run_code(self, src_file: Path, err_file: Path):
        try:
            with open(src_file, "r") as sf:
                code = sf.read()
                exec(code)
        except Exception as e:
            print(str(e))
            with open(err_file, "w") as errf:
                errf.write(str(e))
def get_test_manager() -> TestManager:
    return TestManager()
