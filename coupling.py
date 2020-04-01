
# High coupling examples
# Inheritance instead of composition
# Instantiating dependencies in classes (even with dependencies passed to the constructor of the dependency)

# https://thebojan.ninja/2015/04/08/high-cohesion-loose-coupling/
# https://blog.ndepend.com/programming-coupling/


# Total runtime of time periods in a batch
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List


@dataclass
class TimePeriod:
    start: datetime
    end: datetime

    wafer_id: str

    def get_wafer_processing_duration(self) -> timedelta:
        return self.end - self.start


@dataclass
class Batch:
    time_periods: List[TimePeriod]

    def get_total_processing_duration(self) -> timedelta:
        return sum((tp.get_wafer_processing_duration() for tp in self.time_periods), timedelta())


@dataclass
class Schedule:
    batches: List[Batch]

    def get_total_processing_duration(self) -> timedelta:
        return sum((b.get_total_processing_duration() for b in self.batches), timedelta())


def get_total_process_time(schedule: Schedule):
    """This function takes a schedule and returns the total aggregate time spent processing for all wafers in a schedule"""
    total_time = timedelta()
    for batch in schedule.batches:
        for time_period in batch.time_periods:
            total_time += time_period.end - time_period.start


# Key takeaways:
# 1. Why is this highly coupled?
# 2. What would we need to change if we added setup and teardown periods?
# 3. What about monitor wafers?


# Some metric calculation and the use of dicts?