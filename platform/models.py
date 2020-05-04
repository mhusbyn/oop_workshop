from dataclasses import dataclass
from datetime import datetime, timedelta
from random import random
from typing import List, Optional, Dict


@dataclass
class Job:
    metadata: dict
    wafer_id: str


class Machine:
    def __init__(self):
        self._processing_time = timedelta(hours=random.random())

    @property
    def processing_time(self) -> timedelta:
        return self._processing_time


class File:
    pass


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

