from datetime import timedelta
from typing import List
from platform.data_getter_exercise.data_getter import OptimisationDataGetter
from platform.models import Job, Schedule
from platform.scheduling_exercise.scheduler import OptimisationRunner


class JobPreprocessor:
    def preprocess_jobs(self, jobs: List[Job]):
        for job in jobs:
            job.metadata['next_step_start'] = job.metadata['estimated_next_step_start'] + timedelta(minutes=10)


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

        # Optimisation run
        optimisation_runner = OptimisationRunner()
        schedule = optimisation_runner.run_optimisation(opt_data)

        # Metrics calculator that relies on metadata in preprocessor
        schedule_analyser = ScheduleAnalyser()
        schedule.metrics = schedule_analyser.analyse_schedule(schedule=schedule)

        return schedule
