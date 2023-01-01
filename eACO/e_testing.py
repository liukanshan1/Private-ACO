from eACO.utils import saveSpacePlot, savePathPlot, saveResultsTxt, msg
from e_library import *


def test(tsp):
    """
        Run Ant Colony Optimization (ACO) algorithm for a given Symmetric traveling salesman problem (TSP)
        @arg
            {string} tsp    -- The TSP file src name (located in /data folder)

        @export
            {results}       -- Generated files for results
            {plots}         -- Generated files for plots
    """
    # Default arguments
    '''
        iterations {80}     -- Number of iterations (Ending condition)
        colony {50}         -- Number of ants in the colony
        alpha {1.0}         -- Alpha algorithm parameter, more or less weight to a selected distance
        beta {1.0}          -- Beta algorithm parameter, more or less weight to a selected distance
        del_tau {1.0}       -- Delta Tau algorithm parameter, pheromones releasing rate
        rho {0.5}           -- Rho algorithm parameter, pheromones evaporation rate
    '''

    # Configuration vars
    n = 3                   # Repetitions

    # Algorithm Parameters
    iterations = 80
    colony = 50
    alpha = 1
    beta = 1
    del_tau = 1.0
    rho = 0.5

    results = np.zeros(n)   # Store

    # Get TSP data
    src = getTspData('../data/{}.tsp'.format(tsp))
    space = None
    space = np.array(src['node_coord_section'])

    # Inform
    msg('Computing {} times for {}'.format(n, tsp))

    # Save space plot
    saveSpacePlot(tsp, space)

    # Repeat and save path plot for each result
    for i in range(n):
        # Run
        min_path, min_distance = runAcoTsp(space, iterations, colony, alpha, beta, del_tau, rho)

        # Store result
        results[i] = min_distance

        # Save path plot
        savePathPlot(i, n, tsp, space, min_path, min_distance)

    # Save results txt
    saveResultsTxt(src, results, iterations, colony, alpha, beta, del_tau, rho)




def main():
    # Test for each stored TSP data
    test('kroA100')
    test('berlin52')

    # Inform
    msg('All files generated, see /results for details')


if __name__ == '__main__':
    main()
