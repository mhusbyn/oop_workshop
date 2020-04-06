import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, NewType, Optional


@dataclass
class Job:
    metadata: dict

    start: datetime = None
    end: datetime = None


class Machine:
    pass


class File:
    pass


@dataclass
class Batch:
    jobs: List[Job]
    machine: Optional[Machine] = None


@dataclass
class Schedule:
    batches: List[Batch]
    metrics: Optional[Dict] = None


@dataclass
class OptimisationData:
    jobs: List[Job]
    machines: List[Machine]


class CSVFileFTPClient:
    def get_file_data(self, filename: str) -> List[Dict[str, str]]:
        print(f'Getting data from {filename}')
        return []


class OptimisationDataGetter:
    def get_data(self) -> OptimisationData:
        file_client = CSVFileFTPClient() # !Hardcoded class. What would happen if we wanted different datasources?
        jobs_data = file_client.get_file_data('jobs.csv')
        jobs = [Job(metadata={}) for _ in jobs_data]

        machines_data = file_client.get_file_data('machines.csv')
        machines = [Machine() for _ in machines_data]

        return OptimisationData(jobs=jobs, machines=machines)


class JobPreprocessor:
    def preprocess_jobs(self, jobs: List[Job]):
        for job in jobs:
            job.metadata['next_step_start'] = job.metadata['estimated_next_step_start'] + timedelta(minutes=10)


FrobnicationValue = NewType('FrobnicationValue', float)


class OptimisationRunner:
    def run_optimisation(self, opt_data: OptimisationData) -> List[Tuple[Batch, FrobnicationValue]]:
        batches = []
        start_time = datetime(2020, 1, 1)
        cur_end_time = start_time
        for i in range(0, len(opt_data.jobs), 5):
            batch = Batch(opt_data.jobs[i:i + 5])

            for j in batch.jobs:
                j.start = cur_end_time
                j.end = cur_end_time + timedelta(minutes=20)

            cur_end_time = batch.jobs[0].end

            batches.append((batch, FrobnicationValue(random.random())))

        return batches


class ScheduleBuilder:
    def build_schedule(self, opt_data: OptimisationData, batch_frobnication: List[Tuple[Batch, FrobnicationValue]]):
        # Frobnication value decides the machine
        machines = opt_data.machines
        num_machines = len(machines)
        for batch, frobnication_value in batch_frobnication:
            machine_idx = int(frobnication_value * num_machines)
            batch.machine = machines[machine_idx]

        return Schedule([b for b, _ in batch_frobnication])


class ScheduleAnalyser:
    def analyse_schedule(self, schedule: Schedule):
        total_post_wait_time = timedelta()
        for batch in schedule.batches:
            for job in batch.jobs:
                total_post_wait_time += job.metadata['next_step_start'] - job.end

        return {'total_post_wait_time': total_post_wait_time}


class E2EScheduler:
    def create_schedule(self) -> Schedule:
        data_getter = OptimisationDataGetter()
        opt_data = data_getter.get_data()

        # Preprocessor that adds some metadata
        job_preprocessor = JobPreprocessor()
        job_preprocessor.preprocess_jobs(opt_data.jobs)

        # Optimisation run
        optimisation_runner = OptimisationRunner()
        batches = optimisation_runner.run_optimisation(opt_data)

        # Schedule creator
        schedule_builder = ScheduleBuilder()
        schedule = schedule_builder.build_schedule(opt_data, batches)

        # Metrics calculator that relies on metadata in preprocessor
        schedule_analyser = ScheduleAnalyser()
        schedule.metrics = schedule_analyser.analyse_schedule(schedule=schedule)

        return schedule



# Want to cover:

# Law of Demeter
# Dependency injection
# Long dict coupling
# Unnecessary inheritance
