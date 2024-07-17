from dataclasses import dataclass, field
from typing import Sequence, Optional

import mk_build.config as config
from mk_build.build.path import PathInput
from mk_build.gup import gup
from .process import CompletedProcess
from ..validate import ensure_type


@dataclass
class Target:
    name: Optional[str] = str(config.get().target)
    sources: Sequence[PathInput] = field(default_factory=list)
    dependencies: list[PathInput] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.dependencies += self.sources

    def update(self) -> CompletedProcess[bytes]:
        print(self.name)

        for i in self.dependencies:
            result = ensure_type(gup(i), CompletedProcess)

        return result

    def __str__(self) -> str:
        return (f'Target(name={self.name} sources={self.sources}'
                f' dependencies={self.dependencies})')
