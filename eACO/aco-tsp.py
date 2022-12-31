from library import *
import matplotlib.pyplot as plt


# Get TSP data
TSP = getTspData('../data/kroA100.tsp')

# Display TSP file headers
displayTspHeaders(TSP)

# ### Space
# We can use now its coordenates pairs to plot nodes, this representation is what is called **space**.

# Get Space
space = np.array(TSP['node_coord_section'])

# Plot nodes
plt.scatter(space[:, 0], space[:, 1], s = 15)

# Plot properties
plt.title('Space {}'.format(TSP['name']))
plt.xlabel('Latitude')
plt.ylabel('Longitude')

# Show plot
plt.show()
plt.close()


# Run ACO
min_path, min_distance = runAcoTsp(space)

# Plot path
plt.scatter(space[:, 0], space[:, 1], marker='o', s=15)
plt.plot(space[min_path, 0], space[min_path, 1], c='g', linewidth=0.8, linestyle="--")

# Plot properties
plt.suptitle('Mininum Path')
plt.title('For a minimum distance of {}'.format(min_distance), fontsize = 10)
plt.xlabel('Latitude')
plt.ylabel('Longitude')

# Show plot
plt.show()
plt.close()


# Vars
n = 3 
average = 0 

# Repeat
for i in range(n):
    # Call
    min_path, min_distance = runAcoTsp(space)
    average += min_distance 
    
    # Plot path
    plt.scatter(space[:, 0], space[:, 1], marker='o', s=15)
    plt.plot(space[min_path, 0], space[min_path, 1], c='g', linewidth=0.8, linestyle="--")

    # Plot properties
    plt.suptitle('Mininum Path for {}'.format(TSP['name']))
    plt.title('Result #{} of {} for a minimum distance of {}'.format(i + 1, n, min_distance), fontsize = 10)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
        
    plt.show()
    plt.close()
    
# Show Average
print('Min Distance Average for the last {} results is {}'.format(n, average/n))


# Get TSP data
TSP = getTspData('../data/berlin52.tsp')

# Display TSP file headers
displayTspHeaders(TSP)

# Get Space
space = np.array(TSP['node_coord_section'])

# Plot nodes
plt.scatter(space[:, 0], space[:, 1], s = 15)

# Plot properties
plt.title('Space {}'.format(TSP['name']))
plt.xlabel('Latitude')
plt.ylabel('Longitude')

# Show plot
plt.show()
plt.close()

# Algorithm Parameters
iterations = 50
colony = 25
alpha = 1
beta = 1
del_tau = 1.5
rho = 0.5

# Vars
average = 0 

# Repeat
for i in range(n):
    # Run
    min_path, min_distance = runAcoTsp(space, iterations, colony, alpha, beta, del_tau, rho)
    average += min_distance
    
    # Plot path
    plt.scatter(space[:, 0], space[:, 1], marker='o', s=15)
    plt.plot(space[min_path, 0], space[min_path, 1], c='g', linewidth=0.8, linestyle="--")

    # Plot properties
    plt.suptitle('Mininum Path for {}'.format(TSP['name']))
    plt.title('Result #{} of {} for a minimum distance of {}'.format(i + 1, n, min_distance), fontsize = 10)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
        
    plt.show()
    plt.close()
    
# Show Average
print('Min Distance Average for the last {} results is {}'.format(n, average/n))