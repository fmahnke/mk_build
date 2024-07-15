from dataclasses import dataclass, field
from typing import Sequence, Optional

import mk_build.config as config
from mk_build.build.path import PathInput
from mk_build.gup import gup


@dataclass
class Target:
    name: Optional[str] = config.get().target
    sources: Sequence[PathInput] = field(default_factory=list)
    dependencies: Sequence[PathInput] = field(default_factory=list)

    def __post_init__(self):
        self.dependencies += self.sources

    def update(self) -> None:
        print(self.name)

        for i in self.dependencies:
            gup(i)

    def __str__(self) -> str:
        return (f'Target(name={self.name} sources={self.sources}'
                f' dependencies={self.dependencies})')
