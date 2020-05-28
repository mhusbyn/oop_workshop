from typing import List, Dict

from platform.models import OptimisationData, Job, Machine


class CSVFileFTPClient:
    def get_file_data(self, filename: str) -> List[Dict[str, str]]:
        print(f'Getting data from {filename}')
        return []


class OptimisationDataGetter:
    def get_data(self) -> OptimisationData:
        file_client = CSVFileFTPClient() # !Hardcoded class. What would happen if we wanted different datasources?
        jobs_data = file_client.get_file_data('jobs.csv')
        jobs = [Job(wafer_id='blah', metadata={}) for _ in jobs_data]

        machines_data = file_client.get_file_data('machines.csv')
        machines = [Machine(id_=row['id']) for row in machines_data]

        return OptimisationData(jobs=jobs, machines=machines)


# Questions:
# 1. Why is this tightly coupled, and where are the couplings?
# 2. What if the format is not CSV but JSON?
# 3. What would you do if we had different data sources? E.g. SQL connection, http endpoint, email, user input
# 4. What if jobs and machines had a different data source?
