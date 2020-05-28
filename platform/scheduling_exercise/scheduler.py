import random
from datetime import datetime, timedelta
from typing import List, Tuple, NewType, Dict

from platform.models import OptimisationData, Batch, Job, Machine, Schedule


class OptimisationRunner:
    def run_optimisation(self, opt_data: OptimisationData, start_time) -> Schedule:
        job_machine_assignment = self._get_job_machine_assigment(opt_data=opt_data)
        machine_job_split = {m: self._split_jobs_into_batches(m, jobs) for m, jobs in job_machine_assignment.items()}
        machine_ordered_job_split = {m: self._order_job_splits(m, job_split) for m, job_split in machine_job_split.items()}
        batches = self._create_batches(machine_job_split_mapping=machine_ordered_job_split, start_date=start_time)

        return Schedule(batches=batches)

    def _get_job_machine_assigment(self, opt_data: OptimisationData) -> Dict[Machine, List[Job]]:
        job_machine_assignment = {m: [] for m in opt_data.machines}
        for job in opt_data.jobs:
            machine = self._get_machine_for_job(opt_data.machines, job)
            job_machine_assignment[machine].append(job)

        return job_machine_assignment

    def _get_machine_for_job(self, machines: List[Machine], job: Job) -> Machine:
        # Simulates an optimisation by randomly picking a machine for the job.
        return random.choice(machines)

    def _split_jobs_into_batches(self, machine: Machine, jobs: List[Job]) -> List[List[Job]]:
        # Simulates an optimisation by assigning jobs to batches randomly.
        batched_jobs = []
        cur_index = 0
        while cur_index < len(jobs):
            num_jobs_to_get = random.randrange(1, 9)
            next_batch = jobs[cur_index:cur_index + num_jobs_to_get]
            batched_jobs.append(next_batch)

            cur_index = cur_index + num_jobs_to_get

        return batched_jobs

    def _order_job_splits(self, machine: Machine, job_splits: List[List[Job]]) -> List[List[Job]]:
        # Orders based on the aggregate priority values of the jobs in each split, most important first.
        # Pretend this is due to the current optimisation model used.
        return sorted(job_splits, key=lambda js: sum(j.metadata.get('priority', 10) for j in js))

    def _create_batches(self, machine_job_split_mapping: Dict[Machine, List[List[Job]]], start_date: datetime) -> List[Batch]:
        batches = []
        for machine, job_splits in machine_job_split_mapping.items():
            cur_time = start_date
            for jobs in job_splits:
                end_time = cur_time + machine.get_duration_for_jobs_in_batch(jobs)
                batches.append(Batch(jobs=jobs, machine=machine, start=cur_time, end=end_time))
                cur_time = end_time

        return batches


class JobPriorityPreferenceHeuristicRunner(OptimisationRunner):
    def _get_machine_for_job(self, machines: List[Machine], job: Job) -> Machine:
        try:
            return next(m for m in machines if m.id == job.metadata['preferred_machine'])
        except (KeyError, StopIteration):
            return random.choice(machines)

    def _split_jobs_into_batches(self, machine: Machine, jobs: List[Job]) -> List[List[Job]]:
        """
        Creates batches based on jobs' priorities. Jobs in the same batch all have the same priority.
        When `OptimisationRunner` orders them they will be ordered by priority so the highest priority batches are run
        first.
        """
        batch_allocation: Dict[int, List[Job]] = {}
        no_preference_job_batch = []
        for job in jobs:
            job_priority = job.metadata.get('priority')
            if job_priority is not None:
                try:
                    batch_allocation[job_priority].append(job)
                except KeyError:
                    batch_allocation[job_priority] = [job]
            else:
                no_preference_job_batch.append(job)

        return list(batch_allocation.values()) + [no_preference_job_batch]


# 1. What's the coupling here?
# 2. What if _order_job_splits gets changed in the superclass?
