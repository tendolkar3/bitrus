from simulation import Simulation
from main import Display
import numpy as np
import math
from spaces import DiscreteSpace, BoxSpace

np.random.RandomState(seed=0)


class Env(object):
    def __init__(self):

        # fixme: modify the observation space
        self.observation_space = tuple((BoxSpace(low=0, high=np.inf,shape=(1,)),
                                        BoxSpace(low=0, high=np.inf, shape=(1,)),
                                        DiscreteSpace(n=1),
                                        DiscreteSpace(n=1),
                                        DiscreteSpace(n=1),
                                        DiscreteSpace(n=1),
                                        DiscreteSpace(n=1),
                                        DiscreteSpace(n=1),
                                        ))
        self.action_space = tuple((BoxSpace(low=-math.pi/4, high=math.pi/4, shape=(1,)),
                                   BoxSpace(low=-5, high=5, shape=(1,))))
        self.simulation = Simulation
        self.display = Display(self.simulation)
        self.status = bool

    def step(self, action):
        """
        This should compute one time step of the simulation.
        :param action:
        :return:
        """
        self._take_action(action)

        observation = self._get_observation()
        reward = self._get_reward()
        # if done is True, then terminate the episode. So self.status is False for the episode to terminate.
        # If self.status is True, then the car is in the game, do not terminate.
        done = not self.status
        info = {}

        return observation, reward, done, info

    def _take_action(self, action):

        self.status = self.simulation.sim_step(action)

    def _get_observation(self):

        observation = self.simulation.get_observation()
        return observation

    def _get_reward(self):

        reward = self.simulation.get_reward()
        return reward

    def reset(self):
        """
        reset the environment
        """
        self.simulation = Simulation
        self.display = Display(self.simulation)
        return self.simulation.get_observation()

    def render(self):
        """
        for display
        """
        self.display.draw()

    def seed(self, seed=None):
        """
        pseudo random number generator
        :return:
        """
        pass

