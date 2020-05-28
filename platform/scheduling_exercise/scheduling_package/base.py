import abc
from datetime import datetime
from typing import Dict, List

from platform.models import OptimisationData, Machine, Job


class IScheduler(abc.ABC):
    @abc.abstractmethod
    def create_schedule(self, opt_data: OptimisationData, start_date: datetime):
        pass


# These 3 _might_ require Opt data. Could pass it in constructor if they do. Or change the signature.

class IMachineAssigner(abc.ABC):
    @abc.abstractmethod
    def get_job_machine_assignment(self, opt_data: OptimisationData) -> Dict[Machine, List[Job]]:
        pass


class IBatcher(abc.ABC):
    @abc.abstractmethod
    def split_jobs_into_batches(self, machine: Machine, jobs: List[Job]) -> List[List[Job]]:
        pass


class IBatchSequencer(abc.ABC):
    @abc.abstractmethod
    def order_batches(self, machine: Machine, batches: List[List[Job]]) -> List[List[Job]]:
        pass
