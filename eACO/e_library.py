# [0] Libs
from concurrent.futures import ThreadPoolExecutor
import time

import numpy as np

from eACO.utils import encrypt_2darray, get_fixed_point, decrypt_array, decrypt_2darray, get_fp
from ss.secret import Secret


# [1] TSP
def getTspData(tsp):
    """
        Get data from a given TSP file and convert it into a dictionary
        @arg
            {string} tsp    -- The TSP file src
        @return
            {dictionary}    -- The TSP file as dictionary
    """
    # Open input file
    infile = open(tsp, 'r')

    # Read instance
    name = infile.readline().strip().split()[1]  # NAME
    type = infile.readline().strip().split()[1]  # TYPE
    comment = infile.readline().strip().split()[1]  # COMMENT
    dimension = infile.readline().strip().split()[1]  # DIMENSION
    edge_weight_type = infile.readline().strip().split()[1]  # EDGE_WEIGHT_TYPE
    node_coord_section = []  # NODE_COORD_SECTION
    infile.readline()

    # Read node coord section and store its x, y coordinates
    for i in range(0, int(dimension)):
        x, y = infile.readline().strip().split()[1:]
        node_coord_section.append([float(x), float(y)])

    # Close input file
    infile.close()

    # File as dictionary
    return {
        'name': name,
        'type': type,
        'comment': comment,
        'dimension': dimension,
        'edge_weight_type': edge_weight_type,
        'node_coord_section': node_coord_section
    }


def displayTspHeaders(dict):
    """
        Display headers from a given dictionary gotten from a TSP file
        @arg
            {dictionary} dict   -- TSP to dict converted
    """
    print('\nName: ', dict['name'])
    print('Type: ', dict['type'])
    print('Comment: ', dict['comment'])
    print('Dimension: ', dict['dimension'])
    print('Edge Weight Type: ', dict['edge_weight_type'], '\n')


# [2] ACO
def runAcoTsp(space, iterations=80, colony=50, alpha=1.0, beta=1.0, del_tau=1, rho=0.5):
    """
        Run Ant Colony Optimization (ACO) algorithm for a given Symmetric traveling salesman problem (TSP) space and data
        @arg
            {numpy.ndarray} space           -- The space
            {int} iterations {80}           -- Number of iterations (Ending condition)
            {int} colony {50}               -- Number of ants in the colony
            {float} alpha {1.0}             -- Alpha algorithm parameter, more or less weight to a selected distance
            {float} beta {1.0}              -- Beta algorithm parameter, more or less weight to a selected distance
            {float} del_tau {1.0}           -- Delta Tau algorithm parameter, pheromones releasing rate
            {float} rho {0.5}               -- Rho algorithm parameter, pheromones evaporation rate
        @return
            {Tuple(numpy.ndarray, float)}   -- Indexes of the minimun distance path and the minimun distance
    """
    # 本地阶段
    # 只支持alpha和beta为1
    alpha = 1
    beta = 1
    rho = Secret(int(1 / rho))
    # Find encrypted inverted distances for all nodes
    inv_distances, distances = inverseDistances(space)
    # Add beta algorithm parameter to inverted distances
    inv_distances = (inv_distances ** beta)
    # Empty pheromones trail
    pheromones = encrypt_2darray(np.zeros((space.shape[0], space.shape[0])))
    # 加密参数
    fp = 10 ** get_fixed_point()
    del_tau = Secret(del_tau * fp)
    # 在线阶段
    # Empty minimum distance and path
    min_distance = None
    min_path = None

    # [2] For the number of iterations
    for i in range(iterations):
        print('Iteration: ', i)
        # Initial random positions
        positions = initializeAnts(space.shape, colony)

        # Complete a path
        # [e]space, [p]positions, [e]inv_distances, [e]pheromones, [p]alpha, [p]beta, [e]del_tau
        paths = moveAnts(space.shape, positions, inv_distances, pheromones, alpha, beta, del_tau)

        # Evaporate pheromones
        pheromones = pheromones / rho

        # [3] For each path
        for path in paths:
            # Empty distance
            distance = 0
            # For each node from second to last
            for node in range(1, path.shape[0]):
                # Calculate distance to the last node
                distance += distances[int(path[node]), int(path[node - 1])]

            # Update minimun distance and path if less nor non-existent
            if not min_distance or distance < min_distance:
                min_distance = distance
                min_path = path
                min_path = np.append(min_path, min_path[0])
        print('Iteration: ', i, " ", min_distance.recover() / get_fp())
    # Return tuple
    return min_path, min_distance.recover() / get_fp()


def inverseDistances(space):
    """
        Inverse distance - Get an array of inverted distances
        @arg
            {numpy.ndarray} space   -- The space
        @return
            {numpy.ndarray}         -- A space.dimension per space.dimension array of inverse distances
    """
    # Empty multidimensional array (matriz) to distances
    distances = np.zeros((space.shape[0], space.shape[0]))

    # Calculate distance to all nodes to all nodes
    for index, point in enumerate(space):
        distances[index] = np.sqrt(((space - point) ** 2).sum(axis=1))

    # Floating-point error handling - Setted to known state
    with np.errstate(all='ignore'):
        # Invert the distances
        inv_distances = 1 / distances

    # Replace infinity by zero to prevent zero division error
    inv_distances[inv_distances == np.inf] = 0

    # Eta algorithm result, inverted distances
    return encrypt_2darray(inv_distances), encrypt_2darray(distances)


def initializeAnts(space_shape, colony):
    """
        Initialize ants - Get an array of random initial positions of the ants in space
        @arg
            {numpy.ndarray} space   -- The space
            {int} colony            -- Number of ants in the colony
        @return
            {numpy.ndarry}          -- An array of indexes of initial positions of ants in the space
    """
    # Indexes of initial positions of ants
    return np.random.randint(space_shape[0], size=colony)


def moveAnts(space_shape, positions, inv_distances, pheromones, alpha, beta, del_tau):
    """
        Move ants - Move ants from initial positions to cover all nodes
        @arg
            {numpy.ndarray} space           -- The space
            {numpy.ndarray} positions       -- Indexes of initial positions of ants in the space
            {numpy.ndarray} inv_distances   -- Inverted distances ^ beta
            {numpy.ndarray} pheromones      -- Tau, pheromones trail
            {float} alpha                   -- Alpha algorithm parameter, more or less weight to a selected distance
            {float} beta                    -- Beta algorithm parameter, more or less weight to a selected distance
            {float} del_tau                 -- Delta Tau algorithm parameter, pheromones releasing rate
        @return
            {numpy.ndarry}                  -- Indexes of the paths taken by the ants
    """
    # pool = ThreadPoolExecutor(max_workers=12)

    # Empty multidimensional array (matriz) to paths
    paths = np.zeros((space_shape[0], positions.shape[0]), dtype=int) - 1

    # Initial position at node zero
    paths[0] = positions

    # For nodes after start to end
    for node in range(1, space_shape[0]):
        # future = []
        # For each ant
        for ant in range(positions.shape[0]):
            # f = pool.submit(ant_move, alpha, ant, beta, del_tau, inv_distances, node, paths, pheromones, positions)
            # future.append(f)
            ant_move(alpha, ant, beta, del_tau, inv_distances, node, paths, pheromones, positions)
        # for f in future:
        #     f.result()
    # Paths taken by the ants
    return np.swapaxes(paths, 0, 1)


def ant_move(alpha, ant, beta, del_tau, inv_distances, node, paths, pheromones, positions):
    # Probability to travel the nodes
    # next_location_probability0 = ((inv_distances[positions[ant]] ** alpha + pheromones[positions[ant]] ** beta) * get_fp())/(inv_distances[positions[ant]].sum() ** alpha + pheromones[positions[ant]].sum() ** beta)
    next_location_probability = inv_distances[positions[ant]] ** alpha + pheromones[positions[ant]] ** beta
    for i in range(next_location_probability.shape[0]):
        next_location_probability[i] *= get_fp()
    temp1 = Secret(0)
    for item in inv_distances[positions[ant]]:
        temp1 += item ** alpha
    temp2 = Secret(0)
    for item in pheromones[positions[ant]]:
        temp2 += item ** beta
    temp1 += temp2
    for i in range(next_location_probability.shape[0]):
        next_location_probability[i] = next_location_probability[i].fast_div(temp1)[0]

    # Index to maximum probability node
    next_position = np.argmax(next_location_probability)
    # Check if node has already been visited
    while next_position in paths[:, ant]:
        # Replace the probability of visited to zero
        next_location_probability[next_position] = Secret(0)

        # Find the maximum probability node
        next_position = np.argmax(next_location_probability)
    # Add node to path
    paths[node, ant] = next_position
    # Update pheromones (releasing pheromones)
    pheromones[node, next_position] = pheromones[node, next_position] + del_tau
