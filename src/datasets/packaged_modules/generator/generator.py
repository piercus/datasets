from dataclasses import dataclass
from typing import Callable, Optional

import datasets


@dataclass
class GeneratorConfig(datasets.BuilderConfig):
    generator: Optional[Callable] = None
    gen_kwargs: Optional[dict] = None
    features: Optional[datasets.Features] = None

    def __post_init__(self):
        super().__post_init__()
        if self.generator is None:
            raise ValueError("generator must be specified")

        if self.gen_kwargs is None:
            self.gen_kwargs = {}


class Generator(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = GeneratorConfig

    def __init__(
        self,
        split: Optional[datasets.NamedSplit] = None,
        **kwargs,
    ):
        self.split = split if split is not None else datasets.Split.TRAIN
        return super().__init__(
            **kwargs,
        )

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        return [datasets.SplitGenerator(name=self.split, gen_kwargs=self.config.gen_kwargs)]

    def _generate_examples(self, **gen_kwargs):
        for idx, ex in enumerate(self.config.generator(**gen_kwargs)):
            yield idx, ex
