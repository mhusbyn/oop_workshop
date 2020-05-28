import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, NewType, Optional
from platform.data_getter_exercise.data_getter import OptimisationDataGetter
from platform.models import Job


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

        # Preprocessor that adds some metadata
        job_preprocessor = JobPreprocessor()
        job_preprocessor.preprocess_jobs(opt_data.jobs)

        # Optimisation run
        optimisation_runner = OptimisationRunner()
        schedule = optimisation_runner.run_optimisation(opt_data)

        # Schedule creator
        schedule_builder = ScheduleBuilder()
        schedule = schedule_builder.build_schedule(opt_data, batches)

        # Metrics calculator that relies on metadata in preprocessor
        schedule_analyser = ScheduleAnalyser()
        schedule.metrics = schedule_analyser.analyse_schedule(schedule=schedule)

        return schedule


# Want to cover:

# 45 min each? 30 min work + 15 in discussion

# Law of Demeter (Metrics)
# Dependency injection (data getter)
# Long dict coupling (postprocessing?)
# Unnecessary inheritance (opt model?) (use LSP here?)

# Liskov Substitution principle?
# Encapsulation?
# Cohesion?
