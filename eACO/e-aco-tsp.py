from eACO.stopwatch import Stopwatch
from e_library import *
import matplotlib.pyplot as plt

# Get TSP data
# TSP = getTspData('../data/kroA100.tsp')
TSP = getTspData('../data/berlin52.tsp')

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
# plt.show()
# plt.close()

sw = Stopwatch(3)
sw.start()
# Run ACO
min_path, min_distance = runAcoTsp(space)
print(min_path.shape)
sw.stop()
print(sw)

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

print(min_distance)