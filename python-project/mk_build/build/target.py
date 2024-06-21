from dataclasses import dataclass, field
from typing import Optional

import mk_build.config as config
from mk_build.gup import gup


@dataclass
class Target:
    name: Optional[str] = config.get().target
    sources: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)

    def __post_init__(self):
        self.dependencies += self.sources

    def add_source(self, source):
        self.dependencies.append(source)
        self.sources.append(source)

    def update(self):
        print(self.name)

        for i in self.dependencies:
            gup(i)
