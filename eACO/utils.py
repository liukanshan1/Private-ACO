import numpy as np
import matplotlib.pyplot as plt

from ss.secret import Secret

# Constants
fixed_point = 5
fp = pow(10, fixed_point)


def encrypt_2darray(ndarray: np.array):
    """
    加密numpy数组
    """
    ndarray = (ndarray * fp).astype(np.int64)
    e_ndarray = np.empty(ndarray.shape, dtype=Secret, order='C')
    for i in range(ndarray.shape[0]):
        for j in range(ndarray.shape[1]):
            e_ndarray[i, j] = Secret(ndarray[i, j])
    return e_ndarray


def r_encrypt_2darray(ndarray: np.array):
    """
    加密numpy数组
    """
    ndarray = ndarray.astype(np.int64)
    e_ndarray = np.empty(ndarray.shape, dtype=Secret, order='C')
    for i in range(ndarray.shape[0]):
        for j in range(ndarray.shape[1]):
            e_ndarray[i, j] = Secret(ndarray[i, j])
    return e_ndarray


def decrypt_array(e_array: np.array):
    """
    解密numpy数组
    """
    array = np.zeros(e_array.shape)
    for i in range(array.shape[0]):
        array[i] = e_array[i].recover() / fp
    return array


def decrypt_2darray(e_2darray: np.array):
    array = np.zeros(e_2darray.shape)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i, j] = e_2darray[i, j].recover() / fp
    return array


def saveSpacePlot(tsp, space):
    """
        Save Space plot
        @arg
            {string} tsp            -- The TSP file src name
            {numpy.ndarray} space   -- The space

        @export
            {png}                   -- Generated .png for TSP space plot
    """
    # Plot nodes
    plt.scatter(space[:, 0], space[:, 1], s=15)

    # Plot properties
    plt.title('Space for {}'.format(tsp))
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')

    # Save plot
    file = '../results/{}-space.png'.format(tsp)
    plt.savefig(file)

    # Close plot
    plt.close()

    # Inform
    msg('{} generated'.format(file))


def savePathPlot(i, n, tsp, space, min_path, min_distance):
    """
        Save Path plot for a given result
        @arg
            {int} i                 -- The result
            {int} n                 -- The total results
            {numpy.ndarray}         -- Indexes of the minimun distance path for the result
            {float}                 -- the minimun distance for the result
            {string} tsp            -- The TSP file src name
            {numpy.ndarray} space   -- The space

        @export
            {png}                   -- Generated .png for ACO-TSP path result plot
    """
    # Plot nodes
    plt.scatter(space[:, 0], space[:, 1], marker='o', s=15)
    plt.plot(space[min_path, 0], space[min_path, 1], c='g', linewidth=0.8, linestyle="--")

    # Plot properties
    plt.suptitle('Mininum Path for {}'.format(tsp))
    plt.title('Result #{} of {} for a minimum distance of {}'.format(i + 1, n, min_distance), fontsize=10)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')

    # Save plot
    file = '../results/{}-path-{}.png'.format(tsp, i + 1)
    plt.savefig(file)

    # Close plot
    plt.close()

    # Inform
    msg('{} generated'.format(file))


def saveResultsTxt(src, results, iterations, colony, alpha, beta, del_tau, rho):
    """
        Save results for a given TSP
        @arg
            {dict} src                  -- The TSP file src
            {numpy.ndarray} results     -- The TSP file as dictionary
            {int} iterations {80}       -- Number of iterations (Ending condition)
            {int} colony {50}           -- Number of ants in the colony
            {float} alpha {1.0}         -- Alpha algorithm parameter, more or less weight to a selected distance
            {float} beta {1.0}          -- Beta algorithm parameter, more or less weight to a selected distance
            {float} del_tau {1.0}       -- Delta Tau algorithm parameter, pheromones releasing rate
            {float} rho {0.5}           -- Rho algorithm parameter, pheromones evaporation rate

        @export
            {txt}                       -- Generated .txt for ACO-TSP results
    """
    # Open or create
    file = '../results/{}-results.txt'.format(src['name'])
    txt = open(file, 'w+')

    # Write file
    txt.write('\n--------------------------')
    txt.write('\n 1- TSP INFO')
    txt.write('\n--------------------------')
    txt.write('\nNAME           : {}.tsp (stored in /data)'.format(src['name']))
    txt.write('\n# OF NODES     : {}\n'.format(src['dimension']))

    txt.write('\n--------------------------')
    txt.write('\n 2- ALGORITHM PARAMETERS')
    txt.write('\n--------------------------')
    txt.write('\nITERATIONS     : {}'.format(iterations))
    txt.write('\nCOLONY         : {}'.format(colony))
    txt.write('\nALPHA          : {}'.format(alpha))
    txt.write('\nBETA           : {}'.format(beta))
    txt.write('\nDEL_TAU        : {}'.format(del_tau))
    txt.write('\nRHO            : {}\n'.format(rho))

    txt.write('\n--------------------------')
    txt.write('\n 3- RESULTS ')
    txt.write('\n--------------------------')
    txt.write('\nMIN_DISTANCES      : {}'.format(results))
    txt.write('\n# OF RESULTS       : {}'.format(results.size))
    txt.write('\nAVG_MIN_DISTANCE   : {}'.format(np.average(results)))
    txt.write('\n--------------------------')

    # Close file
    txt.close()

    # Inform
    msg('{} generated'.format(file))


def msg(str):
    """
        Show a console message
        @arg
            {string} str
    """
    print('[Testing ACO_TSP] {}'.format(str))


def get_fixed_point():
    return fixed_point


def get_fp():
    return fp
