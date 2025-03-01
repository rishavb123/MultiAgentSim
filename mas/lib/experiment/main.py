from omegaconf import OmegaConf

from experiment_lab.core import run_experiment

from mas.lib.experiment.config import MultiAgentSimConfig, register_configs
from mas.lib.experiment.experiment import MultiAgentSimExperiment

if __name__ == "__main__":
    run_experiment(
        experiment_cls=MultiAgentSimExperiment,
        config_cls=MultiAgentSimConfig,
        register_configs=register_configs,
        config_path="./configs",
        config_name="mas",
    )
