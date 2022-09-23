from __future__ import annotations
import subprocess
from typing import TypedDict, List


Deployment = TypedDict("Deployment", {
    "az": None,
    "functionapp": None,
    "deployment": None,
    "source": None,
    "config-zip": None,
    "name": str,
    "resource_group": str,
    "src": str,
})

Create = TypedDict("Create", {
    "az": None,
    "functionapp": None,
    "create": None,
    "name": str,
    "storage_account": str,
    "consumption_plan_location": str,
    "resource_group": str,
    "os_type": str,
    "runtime": str,
    "runtime_version": str,
    "functions_version": str,
})

Delete = TypedDict("Delete", {
    "az": None,
    "functionapp": None,
    "delete": None,
    "--yes": None,
    "name": str,
    "resource_group": str,
})


class FunctionApp:

    def __init__(self) -> None:
        self.command = []
        self.options = []

    def _generate_command(self, type) -> List[str]:
        command = [k for k, v in type.__annotations__.items() if v is None.__class__]
        return command
    
    def _generate_options(self, settings: dict) -> List[str]:
        keys = ["--%s" % k.replace('_', '-') for k in [*settings.keys()]]
        values = [*settings.values()]
        # Flatten 2D array to one dimension
        options = sum([[option, arg] for option, arg in zip(keys, values)], [])
        return options

    def deployment(self, settings: Deployment) -> FunctionApp:
        self.command = self._generate_command(Deployment)
        self.options = self._generate_options(settings)
        return self

    def create(self, settings: Create) -> FunctionApp:
        self.command = self._generate_command(Create)
        self.options = self._generate_options(settings)
        return self

    def delete(self, settings: Delete) -> FunctionApp:
        self.command = self._generate_command(Delete)
        self.options = self._generate_options(settings)
        return self

    def run(self) -> None:
        subprocess.run(self.command + self.options)
