from typing import Any

from experiment_lab.core.base_experiment import BaseExperiment
import hydra

from mas.lib.experiment.config import MultiAgentSimConfig


class MultiAgentSimExperiment(BaseExperiment):

    def __init__(self, cfg: MultiAgentSimConfig) -> None:
        self.cfg = cfg
        self.initialize_experiment()

    def initialize_experiment(self) -> None:
        super().initialize_experiment()
        # self.env = hydra.utils.instantiate(self.cfg.env)

    def single_run(
        self, run_id: str, run_output_path: str, seed: int | None = None
    ) -> Any:
        print("hello")
