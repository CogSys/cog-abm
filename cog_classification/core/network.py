import random

from cog_classification.core.behavior_switcher import BehaviorSwitcher


class Network(BehaviorSwitcher):
    """
    This class implements set of agents with changing topology.

    :param dictionary agents: dictionary of agents in which agents names are keys and agents are values.
    :param dictionary topologies: \
        dictionary of topologies in which times since when topologies is activated are the keys \
        and topologies are values. \
        Topology is represented as dictionary in which agents names are the keys \
        and lists of neighbours agents names are values.
    """

    def __init__(self, agents, topologies):
        BehaviorSwitcher.__init__(self, topologies)
        self.agents = agents

    def get_agent(self):
        """
        :return: random agent from network.
        :rtype: Agent
        """
        return random.choice(self.agents.values())

    def get_agents(self, number_of_agents):
        """"
        Returns list of names of agents.

        :param long number_of_agents: the length of necessary list.

        :return: list of agents in which each two agent are connected by path created by other agents in list.
        :rtype: list of Agents

        Each two agents in list are connected by the path created by agents in list.
        | If in network are isolated subgraph of size less than number of agent then this method can return empty list.
        """
        # agents will contains all chosen agents. agents type - list of Agents.
        agents = []
        agents_names = []
        candidates = []

        # Choosing firs agent.
        agent_name = random.choice(self.agents.keys())
        agents.append(self.agents[agent_name])
        agents_names.append(agent_name)

        current_topology = self.current_behavior
        candidates += current_topology[agent_name]

        # Choosing other agents.
        for _ in range(number_of_agents - 1):

            if len(candidates) < 1:
                return []
            else:
                new_agent = random.choice(candidates)
                candidates = [agent for agent in candidates if not agent == new_agent]

                agent_name = new_agent
                agents.append(self.agents[agent_name])
                agents_names.append(agent_name)

                # We want to add to candidates only the neighbours of new agent
                # that aren't in chosen agents and candidates.
                agents_not_chosen_yet = set(current_topology[agent_name]) - set(agents)
                candidates += list(agents_not_chosen_yet - set(candidates))

        return agents

    def get_all_agents(self):
        """
        :return: all network's agents.
        :rtype: list of Agents
        """
        return self.agents.values()
