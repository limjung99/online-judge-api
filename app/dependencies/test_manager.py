import os
import sys
from multiprocessing import process
class TestManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TestManager,cls).__new__(cls,*args,**kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self,"_inited"):
            self._inited = True

    def check_not_allowed_syscall(self)->bool:
        # check not allowed syscall from src
        # TODO : some logic check not allowed syscall
        return False

    def run_test(self,src:str,example_input:str,expected_output:str)->bool:
        # Run TEST
        if self.check_not_allowed_syscall(src):
            return False

        read_pipe,write_pipe = os.pipe()
        pid = os.fork()

        if pid == 0:
            # Child process
            os.close(read_pipe)
            os.dup2(write_pipe, sys.stdout.fileno())
            os.dup2(write_pipe, sys.stderr.fileno())
            os.dup2(write_pipe, sys.stdin.fileno())

            try:
                exec(src, {'__name__': '__main__'})
            except Exception as e:
                print(e)

            os._exit(0)
        else:
            os.close(write_pipe)
            os.write(read_pipe, example_input.encode())
            os.close(read_pipe)
            os.waitpid(pid, 0)
            output = os.read(read_pipe, 1024).decode()
            os.close(read_pipe)

            return output.strip() == expected_output.strip()


def get_test_manager()->TestManager:
    return TestManager()
