
import numpy as np
import matplotlib.pyplot as plt

def generate_even_hexagonal_grid(n, width, height):
    points = []
    hex_height = np.sqrt(3)  # Height of the hexagon
    hex_width = 1  # Width of the hexagon

    # Calculate rows and columns based on hexagonal packing
    cols = int(np.floor(width / hex_width))
    rows = int(np.floor(height / hex_height))

    # Generate points in the hexagonal grid
    for row in range(rows):
        for col in range(cols):
            x = col * hex_width
            y = row * hex_height

            # Offset for every second row to create hexagonal packing
            if row % 2 == 1:
                x += hex_width / 2

            points.append((x, y))

    # If we have fewer than n points, extend the grid
    while len(points) < n:
        rows += 1
        for row in range(rows):
            for col in range(cols):
                x = col * hex_width
                y = row * hex_height

                if row % 2 == 1:
                    x += hex_width / 2

                if (x, y) not in points:
                    points.append((x, y))
                    if len(points) >= n:
                        break
            if len(points) >= n:
                break

    # Randomly select n points from the g


# Parameters
n = 100  # Number of points
width = 10  # Width of the area
height = 10  # Height of the area

# Generate points
hex_points = generate_even_hexagonal_grid(n, width, height)

# Plot the points
x_coords, y_coords = zip(*hex_points)
plt.scatter(x_coords, y_coords, marker='o')
plt.xlim(0, width)
plt.ylim(0, height)
plt.gca().set_aspect('equal', adjustable='box')
plt.title(f'Even Hexagonally Distributed Points: {len(hex_points)} Points')
plt.xlabel('Width')
plt.ylabel('Height')
plt.grid()
plt.show()
