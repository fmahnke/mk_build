from dataclasses import dataclass, field
from typing import MutableSequence, Optional

import mk_build.config as config
from mk_build.build.path import PathInput
from mk_build.gup import gup


@dataclass
class Target:
    name: Optional[str] = config.get().target
    sources: MutableSequence[PathInput] = field(default_factory=list)
    dependencies: MutableSequence[PathInput] = field(default_factory=list)

    def __post_init__(self):
        self.dependencies += self.sources

    def add_source(self, source) -> None:
        self.dependencies.append(source)
        self.sources.append(source)

    def update(self) -> None:
        print(self.name)

        for i in self.dependencies:
            gup(i)
