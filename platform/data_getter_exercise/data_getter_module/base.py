import abc
from typing import Iterable, Dict, Any

from platform.data_getter_exercise.data_getter_module.readers import IDataReader
from platform.models import OptimisationData, Machine, Job


class IOptimisationDataGetter(abc.ABC):
    @abc.abstractmethod
    def get_data(self) -> OptimisationData:
        pass


class IJobGetter(abc.ABC):
    @abc.abstractmethod
    def get_jobs(self) -> Iterable[Job]:
        pass


class IMachineGetter(abc.ABC):
    @abc.abstractmethod
    def get_machines(self) -> Iterable[Machine]:
        pass


class BaseMachineGetter(IMachineGetter):
    def __init__(self, data_getter: IDataReader, parser: 'MachineParser'):
        self._data_getter = data_getter
        self._parser = parser

    def get_machines(self) -> Iterable[Machine]:
        for datum in self._data_getter.get_data():
            yield self._parser.parse_machine_dict(datum)


class BaseJobGetter(IJobGetter):
    def __init__(self, data_getter: IDataReader, parser: 'JobParser'):
        self._data_getter = data_getter
        self._parser = parser

    def get_jobs(self) -> Iterable[Job]:
        for datum in self._data_getter.get_data():
            yield self._parser.parse_job_dict(datum)


class MachineParser:
    def __init__(self, mapping: Dict[str, str]):
        self._mapping = mapping

    def parse_machine_dict(self, machine_dict: Dict[str, str]) -> Machine:
        # map values passed in the machine dict to values for params for the Machine constructor
        # Potentially cast/parse to the right type
        return Machine()


class JobParser:
    def __init__(self, mapping: Dict[str, str]):
        self._mapping = mapping

    def parse_job_dict(self, job_dict: Dict[str, str]):
        # map values passed in the job dict to values for params for the Job constructor
        job_constructor_params: Dict[str, Any] = {}
        for key, value in job_dict:
            constructor_key = self._mapping[key]
            if constructor_key.startswith('metadata'):
                metadata_str, metadata_key = constructor_key.split('.')
                job_constructor_params['metadata'][metadata_key] = value
                continue

            job_constructor_params[constructor_key] = value
            # Potentially cast/parse to the right type

        return Job(metadata=job_constructor_params['metadata'], wafer_id=job_constructor_params['wafer_id'])


class SeparateJobMachineGetter(IOptimisationDataGetter):
    def __init__(self, job_getter: 'IJobGetter', machine_getter: 'IMachineGetter'):
        self._job_getter = job_getter
        self._machine_getter = machine_getter

    def get_data(self) -> OptimisationData:
        jobs = self._job_getter.get_jobs()
        machines = self._machine_getter.get_machines()
        return OptimisationData(jobs=list(jobs), machines=list(machines))

