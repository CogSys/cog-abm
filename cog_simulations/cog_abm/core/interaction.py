

class Interaction(object):

    @staticmethod
    def num_agents():
        """
        Should return number of agents taking part in interaction
        """
        pass

    def interact(self, *agents):
        """
        Does interaction with given agents
        """
        pass

    def change_environment(self, environment):
        """
        Changes environment of interaction
        """
        pass
