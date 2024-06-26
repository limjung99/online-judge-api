
class TestManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TestManager,cls).__new__(cls,*args,**kwargs)
        return cls._instance
    def __int__(self):
        if not hasattr(self,"_inited"):
            self._inited = True
            # TODO : something init once

    def run_test(self,test_id:int,test_input:str)->bool:
        # Run TEST
        pass