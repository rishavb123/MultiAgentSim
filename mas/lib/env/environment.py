from abc import ABC, abstractmethod
from typing import List, Any, Dict
import time
import uuid

from mas.lib.env.entity import Entity
from mas.lib.env.agent import Agent


class Environment(ABC):

    STATE_TYPE = None
    ACTION_TYPE = None

    def __init__(
        self,
        agents: List[Agent] | None = None,
        entities: List[Entity] | None = None,
        render_mode: str | None = None,
        max_fps: float | None = None,
        max_steps_per_episode: int | None = None,
    ):
        agents = [] if agents is None else agents
        entities = [] if entities is None else entities
        self.agents = {
            agent.id: agent for agent in agents
        }  # Store agents in a dictionary
        self.entities = {
            entity.id: entity for entity in entities
        }  # Store agents in a dictionary
        self.state = None
        self.render_mode = render_mode
        self.min_step_time = None if max_fps is None else 1 / max_fps
        self.max_steps_per_episode = max_steps_per_episode
        self.reset()

    @abstractmethod
    def initialize_state(self):
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    def reset(self) -> None:
        self.initialize_state()
        self.cur_step = 0
        self.render()
        self.last_step_time = time.time() - self.min_step_time

    @abstractmethod
    def update_state(
        self, agent_actions: Dict[uuid.UUID, Any], entity_updates: Dict[uuid.UUID, Any]
    ) -> None:
        pass

    def cleanup(self):
        agent_ids_to_kill = set(agent_id for agent_id, agent in self.agents.items() if agent.should_kill())
        for agent_id_to_kill in agent_ids_to_kill:
            self.agents[agent_id_to_kill].kill()
            del self.agents[agent_id_to_kill]
        entity_ids_to_kill = set(entity_id for entity_id, entity in self.agents.items() if entity.should_kill())
        for entity_id_to_kill in entity_ids_to_kill:
            self.entities[entity_id_to_kill].kill()
            del self.entities[entity_id_to_kill]

    def step(self):
        if self.is_done():
            return self.state, True

        cur_time = time.time()
        if (
            self.min_step_time is not None
            and cur_time - self.last_step_time < self.min_step_time
        ):
            time.sleep(self.min_step_time - (cur_time - self.last_step_time))
            cur_time = self.last_step_time + self.min_step_time
        self.last_step_time = cur_time

        observations = {
            agent_id: agent.observe(self.state)
            for agent_id, agent in self.agents.items()
        }
        agent_actions = {
            agent_id: self.agents[agent_id].compute_action(obs)
            for agent_id, obs in observations.items()
        }
        entity_updates = {
            entity_id: self.entities[entity_id].update() for entity_id in self.entities
        }
        self.update_state(agent_actions=agent_actions, entity_updates=entity_updates)
        for agent_id, agent in self.agents.items():
            self.agents[agent_id].update(self.state, agent.observe(self.state))
        self.render()
        self.cleanup()
        return self.state

    def run(self):
        while not self.is_done():
            self.step()
