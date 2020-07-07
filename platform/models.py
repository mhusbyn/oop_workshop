from dataclasses import dataclass
from datetime import datetime, timedelta
from random import random
from typing import List, Optional, Dict


@dataclass
class Job:
    metadata: Dict
    wafer_id: str


class Machine:
    def __init__(self, id_: str):
        self._processing_time_modifier = random.random()
        self._id = id_

    @property
    def processing_time(self) -> float:
        """Modifier that captures the 'efficiency' of a machine. Should be multiplied with any processing times
        from batches"""
        return self._processing_time_modifier

    def get_duration_for_jobs_in_batch(self, jobs: List[Job]) -> timedelta:
        return (FIXED_BATCH_TIME + len(jobs) * VARIABLE_BATCH_TIME) * self._processing_time_modifier

    @property
    def id(self):
        return self._id


FIXED_BATCH_TIME = timedelta(minutes=10)
VARIABLE_BATCH_TIME = timedelta(minutes=2)


@dataclass
class Batch:
    jobs: List[Job]
    machine: Machine

    start: datetime
    end: datetime


@dataclass
class Schedule:
    batches: List[Batch]
    metrics: Optional[Dict] = None


@dataclass
class OptimisationData:
    jobs: List[Job]
    machines: List[Machine]

