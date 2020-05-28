from datetime import datetime
from typing import Dict, List

from platform.models import OptimisationData, Machine, Job, Batch, Schedule
from platform.scheduling_exercise.scheduling_package.base import IScheduler, IMachineAssigner, IBatcher, IBatchSequencer


class ComposedScheduler(IScheduler):
    def __init__(self, machine_assigner: IMachineAssigner, batcher: IBatcher, sequencer: IBatchSequencer):
        self._machine_assigner = machine_assigner
        self._batcher = batcher
        self._sequencer = sequencer

    def create_schedule(self, opt_data: OptimisationData, start_date: datetime):
        job_machine_assignment = self._machine_assigner.get_job_machine_assignment(opt_data=opt_data)
        machine_job_split = {m: self._batcher.split_jobs_into_batches(m, jobs) for m, jobs in job_machine_assignment.items()}
        machine_ordered_job_split = {m: self._sequencer.order_batches(m, job_split) for m, job_split in machine_job_split}
        batches = self._create_batches(machine_job_split_mapping=machine_ordered_job_split, start_date=start_date)

        return Schedule(batches=batches)

    def _create_batches(self, machine_job_split_mapping: Dict[Machine, List[List[Job]]], start_date: datetime) -> List[Batch]:
        batches = []
        for machine, job_splits in machine_job_split_mapping.items():
            cur_time = start_date
            for jobs in job_splits:
                end_time = cur_time + machine.get_duration_for_jobs_in_batch(jobs)
                batches.append(Batch(jobs=jobs, machine=machine, start=cur_time, end=end_time))
                cur_time = end_time

        return batches

