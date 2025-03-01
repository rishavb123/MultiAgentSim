from typing import Dict
from enum import Enum
import numpy as np
import uuid

from mas.lib.env.environment import Environment
from mas.lib.env.agent import Agent


class RPSAction(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class RPSEnv(Environment):

    STATE_TYPE = uuid.UUID | None
    ACTION_TYPE = RPSAction

    def __init__(self, agents=None, render_mode="text", max_fps=1):
        assert agents is not None and len(agents) == 2
        super().__init__(
            agents=agents, entities=None, render_mode=render_mode, max_fps=max_fps
        )

    def initialize_state(self):
        self.state = dict(winner=None, last_actions=None)

    def is_done(self):
        return self.state["winner"] is not None

    def update_state(self, agent_actions, entity_updates):
        agent1_id, agent2_id = tuple(agent_actions.keys())
        agent1_action, agent2_action = (
            agent_actions[agent1_id],
            agent_actions[agent2_id],
        )
        self.state["winner"] = [None, agent1_id, agent2_id][
            (agent1_action.value - agent2_action.value) % 3
        ]
        self.state["last_actions"] = agent_actions

    def render(self):
        if self.render_mode == "text" and self.state["last_actions"] is not None:
            print("=" * 50)
            print(f"Winner: {self.state['winner']}")
            for agent_id, action in self.state["last_actions"].items():
                print(f"{action} from {agent_id}")
            print("=" * 50)
            print()


class RPSAgent(Agent):
    def __init__(
        self,
        probs: Dict[RPSEnv.ACTION_TYPE, float] | None = None,
        learning: bool = False,
    ):
        super().__init__()
        self.probs = (
            {a: 1 / len(list(RPSEnv.ACTION_TYPE)) for a in list(RPSEnv.ACTION_TYPE)}
            if probs is None
            else probs
        )
        self.learning = learning
        assert not self.learning, "learning not implemented yet"

    def observe(self, state: RPSEnv.STATE_TYPE) -> None:
        return None

    def compute_action(self, observation):
        return np.random.choice(
            list(RPSEnv.ACTION_TYPE),
            p=[self.probs[a] for a in list(RPSEnv.ACTION_TYPE)],
        )

    def update(self, state: RPSEnv.STATE_TYPE, observation: None):
        if self.learning:
            pass  # TODO: implement some sort of update here


if __name__ == "__main__":
    RPSEnv(agents=[RPSAgent(), RPSAgent()], render_mode="text", max_fps=1).run()
