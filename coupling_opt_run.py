from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict


@dataclass
class Job:
    metadata: dict

    start: datetime = None
    end: datetime = None


class Machine:
    pass


class File:
    pass


class Schedule:
    pass


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


class E2EScheduler:
    def create_schedule(self) -> Schedule:
        data_getter = OptimisationDataGetter()
        opt_data = data_getter.get_data()

        # Preprocessor that adds some metadata
        job_preprocessor = JobPreprocessor()
        job_preprocessor.preprocess_jobs(opt_data.jobs)

        # Optimisation run

        # Metrics calculator that relies on metadata in preprocessor

        # Schedule creator

        pass
