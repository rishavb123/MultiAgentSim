from typing import Any, Dict

from dataclasses import dataclass

from hydra.core.config_store import ConfigStore
from experiment_lab.core import BaseConfig, BaseExperiment, run_experiment


@dataclass
class MultiAgentSimConfig(BaseConfig):
    pass


def register_configs():
    cs = ConfigStore.instance()
    cs.store(name="mas_config", node=MultiAgentSimConfig)
