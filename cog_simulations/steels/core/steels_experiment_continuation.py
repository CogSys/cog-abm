from steels_experiment import load_environment


def steels_experiment_continuation(simulation, old_params, new_params):

    # Changing parameters to suit whole new simulation.
    old_params["num_iter"] += new_params["num_iter"]

    old_iteration = simulation.get_iteration_counter()
    for network in new_params["networks"]:
        network["start"] += old_iteration - 1
        old_params["networks"].append(network)

    simulation.set_networks(old_params["networks"])

    colour_order, environments = load_environment(new_params["environments"])
    for environment in environments:
        environment["start"] += old_iteration - 1
        old_params["environments"].append(environment)

    simulation.set_environments(old_params["environments"])
    simulation.set_colour_order(colour_order)

    results = simulation.continue_(new_params["num_iter"], old_params["dump_freq"])

    return results, simulation, old_params
