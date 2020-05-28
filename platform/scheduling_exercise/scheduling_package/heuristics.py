import random
from typing import Dict, List

from platform.models import OptimisationData, Machine, Job
from platform.scheduling_exercise.scheduling_package.base import IMachineAssigner, IBatcher, IBatchSequencer, IScheduler
from platform.scheduling_exercise.scheduling_package.shared import ComposedScheduler


class PreferenceMachineAssigner(IMachineAssigner):
    def get_job_machine_assignment(self, opt_data: OptimisationData) -> Dict[Machine, List[Job]]:
        job_machine_assignment = {m: [] for m in opt_data.machines}
        for job in opt_data.jobs:
            machine = self._get_machine_for_job(opt_data.machines, job)
            job_machine_assignment[machine].append(job)

        return job_machine_assignment

    def _get_machine_for_job(self, machines: List[Machine], job: Job) -> Machine:
        try:
            return next(m for m in machines if m.id == job.metadata['preferred_machine'])
        except (KeyError, StopIteration):
            return random.choice(machines)


class PriorityJobBatcher(IBatcher):
    def split_jobs_into_batches(self, machine: Machine, jobs: List[Job]) -> List[List[Job]]:
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


class PriorityBatchSequencer(IBatchSequencer):
    def order_batches(self, machine: Machine, batches: List[List[Job]]) -> List[List[Job]]:
        return sorted(batches, key=lambda js: sum(j.metadata.get('priority', 10) for j in js))


def get_composed_heuristic_scheduler() -> IScheduler:
    return ComposedScheduler(
        machine_assigner=PreferenceMachineAssigner(),
        batcher=PriorityJobBatcher(),
        sequencer=PriorityBatchSequencer()
    )
