

class Env(object):

    def __init__(self, observation_space, action_space):
        self.observation_space = observation_space
        self.action_space = action_space
        self.simulation = None
        pass

    def step(self, action):
        """
        This should compute one time step of the simulation.
        :param action:
        :return:
        """
        self.simulation.step()
        # simulation.step should return the observation space of the car, the reward obtained from the previous step,etc
        observation = object
        reward = float
        done = bool
        info = dict()

        return observation, reward, done, info
    
    def reset(self):
        """
        reset the environment
        """
        pass

    def render(self):
        """
        for display
        """

    def seed(self, seed=None):
        """
        pseudo random number generator
        :return:
        """


class Space(object):
    """
    a generic space object for both the action space and the observation space
    """

    def sample(self):
        pass

    def contains(self):
        pass


