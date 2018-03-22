# import gym
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from itertools import count
from copy import deepcopy
from PIL import Image
from environment import Env
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
import torchvision.transforms as T
from spaces import BoxSpace, DiscreteSpace


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        else:
            self.memory.__delitem__(0)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(11, 32)
        self.fc2 = nn.Linear(32, 2)
        # self.fc3 = nn.Linear(32, 2)

    def forward(self, x):

        print(x.shape)
        x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        x = self.fc2(x)

        return x


model = DQN()
steps_done = 0


def select_action(state):

    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample < eps_threshold:
        # val, ans = model(Variable(state, volatile=True).type(FloatTensor)).data.max(0) # .data.max(1)[1].view(1,1)
        # print(model(Variable(state, volatile=True).type(FloatTensor)).data)
        # print('as')
        action_space = tuple((BoxSpace(low=-math.pi / 4, high=math.pi / 4, shape=(1,)),
                              BoxSpace(low=-5, high=5, shape=(1,))))
        _action = tuple((action_space[0].sample(), action_space[1].sample()))

        return _action
    else:
        action_space = tuple((BoxSpace(low=-math.pi / 4, high=math.pi / 4, shape=(1,)),
                              BoxSpace(low=-5, high=5, shape=(1,))))
        _action = tuple((action_space[0].sample(), action_space[1].sample()))

        return _action


use_cuda = not torch.cuda.is_available()
FloatTensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor
LongTensor = torch.cuda.LongTensor if use_cuda else torch.LongTensor
ByteTensor = torch.cuda.ByteTensor if use_cuda else torch.ByteTensor
Tensor = FloatTensor
NUM_EPISODES = 10
EPISODE_LENGTH = 1000

env = Env()
# env = gym.make('CartPole-v0').unwrapped
BATCH_SIZE = 128
memory = ReplayMemory(1000)
optimizer = optim.RMSprop(model.parameters())
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200


episode_durations = []


def plot_durations():
    plt.figure(2)
    plt.clf()
    durations_t = torch.FloatTensor(episode_durations)
    plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated


def optimize_model():
    # print('yes')
    if len(memory) < BATCH_SIZE:
        return

    transitions = memory.sample(BATCH_SIZE)
    # print("t",len(transitions))
    batch = Transition(*zip(*transitions))

    non_final_mask = ByteTensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)))
    non_final_next_states = Variable(torch.cat([s for s in batch.next_state
                                                if s is not None]),
                                     volatile=True)
    state_batch = Variable(torch.cat(batch.state))
    action_batch = Variable(torch.cat(batch.action))
    reward_batch = Variable(torch.cat(batch.reward))
    print(model(state_batch).shape, "aa")

    state_action_values = model(state_batch).gather(1, torch.LongTensor([0,1]))
    next_state_values = Variable(torch.zeros(BATCH_SIZE).type(Tensor))
    next_state_values[non_final_mask] = model(non_final_next_states).max(1)[0]
    next_state_values.volatile = False
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values)

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    for param in model.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()


num_episodes = 100
for i_episode in range(num_episodes):
    # Initialize the environment and state
    state = env.reset()
    # print(state[5])
    state = FloatTensor(state).transpose(0,1)
    print(state.shape)

    for t in count():
        # Select and perform an action
        action = select_action(state)
        # print(action, type(action))
        state, reward, done, _ = env.step(action)
        state, reward, done, _ = env.step(action)
        state = FloatTensor(state).transpose(0,1)
        reward = Tensor([reward])

        # Observe new state
        if not done:
            next_state = state
        else:
            next_state = None

        # Store the transition in memory
        memory.push(state, FloatTensor([[action]]), next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the target network)
        optimize_model()
        if done:
            episode_durations.append(t + 1)
            plot_durations()
            break
        else:
            env.render()

print('Complete')
# env.render(close=True)
env.close()
plt.show()
