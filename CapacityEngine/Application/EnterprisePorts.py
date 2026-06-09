from typing import Protocol


class EnterpriseAssessmentRepository(Protocol):
    def SaveEnterpriseDataset(self, Dataset: dict) -> None:
        ...


class EnterpriseMetricRepository(Protocol):
    def SaveEnterpriseSamples(self, LoadId: str, Samples: list[dict]) -> None:
        ...


class EnterpriseInventorySource(Protocol):
    def ListInventoryHosts(self) -> list[dict]:
        ...
