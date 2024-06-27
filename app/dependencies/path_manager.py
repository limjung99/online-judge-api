from pathlib import Path


class PathFactory():
    # test_id와 관련된 path를 생산하는 factory class
    # 절대 경로 반환
    def __init__(self, test_id):
        self.test_id = test_id

    def get_output_path(self) -> Path:
        return Path(f"app/resources/outputs/output{self.test_id}.txt").absolute()
