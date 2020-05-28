import random
from typing import Dict, List

from platform.models import OptimisationData, Machine, Job
from platform.scheduling_exercise.scheduling_package.base import IMachineAssigner, IBatcher, IBatchSequencer, IScheduler
from platform.scheduling_exercise.scheduling_package.shared import ComposedScheduler


class OptimisationMachineAssigner(IMachineAssigner):
    def get_job_machine_assignment(self, opt_data: OptimisationData) -> Dict[Machine, List[Job]]:
        # Simulates an optimisation by randomly assigning a machine to a job.
        job_machine_assignment = {m: [] for m in opt_data.machines}
        for job in opt_data.jobs:
            machine = random.choice(opt_data.machines)
            job_machine_assignment[machine].append(job)

        return job_machine_assignment


class OptimisationBatcher(IBatcher):
    def split_jobs_into_batches(self, machine: Machine, jobs: List[Job]) -> List[List[Job]]:
        # Simulates an optimisation by assigning jobs to batches randomly.
        batched_jobs = []
        cur_index = 0
        while cur_index < len(jobs):
            num_jobs_to_get = random.randrange(1, 9)
            next_batch = jobs[cur_index:cur_index + num_jobs_to_get]
            batched_jobs.append(next_batch)

            cur_index = cur_index + num_jobs_to_get

        return batched_jobs


class OptimisationBatchSequencer(IBatchSequencer):
    def order_batches(self, machine: Machine, batches: List[List[Job]]) -> List[List[Job]]:
        # Orders based on the aggregate priority values of the jobs in each split, most important first.
        # Pretend this is due to the current optimisation model used.
        return sorted(batches, key=lambda js: sum(j.metadata.get('priority', 10) for j in js))


def get_composed_opt_scheduler() -> IScheduler:
    return ComposedScheduler(
        machine_assigner=OptimisationMachineAssigner(),
        batcher=OptimisationBatcher(),
        sequencer=OptimisationBatchSequencer()
    )


class OptimisationScheduler(IScheduler):
    # This would be a more complex scheduler that wouldn't separate machine assignments, job splits and all that.
    # Just here to show how that would be done.
    pass