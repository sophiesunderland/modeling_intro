import numpy as np
import matplotlib.pyplot as plt

# Image size
#width = 800
#height = 700

def plot_triangle(border = 100, width = 800, height = 700, w1 = 0.5, w2 = 0.3, w3 = 0.2):
    """"
    Generate a triangle with a 2D point inside 
    
    Input parameters: shape border, width, and height. Weights corresponding to physical, analytical, and data-driven components.
    
    """
    # Create empty RGB image initialized to white
    image = np.ones((height, width, 3), dtype=float)

    # Triangle vertices
    red_point = np.array([width / 2, border])          # top
    green_point = np.array([100, height - border])     # bottom left
    blue_point = np.array([width - 100, height - border])  # bottom right
    
    def add_point(w1, w2, w3):

        total = w1 + w2 + w3

        # Normalize weights
        w1 = w1 / total
        w2 = w2 / total
        w3 = w3 / total

        # Get coordinate for point
        x = w1 * red_point[0] + w2 * green_point[0] + w3 * blue_point[0]

        y = w1 * red_point[1] + w2 * green_point[1] + w3 * blue_point[1]

        return [x, y]

    def point_in_triangle(p, a, b, c):
        """
        Return True if point p is inside triangle abc.
        Uses barycentric coordinates.
        """
        v0 = c - a
        v1 = b - a
        v2 = p - a

        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        denom = dot00 * dot11 - dot01 * dot01

        u = (dot11 * dot02 - dot01 * dot12) / denom
        v = (dot00 * dot12 - dot01 * dot02) / denom

        return (u >= 0) and (v >= 0) and (u + v <= 1)


# Maximum possible distance inside triangle
    max_dist = max(
    np.linalg.norm(red_point - green_point),
    np.linalg.norm(red_point - blue_point),
    np.linalg.norm(green_point - blue_point),
)

# Loop through every pixel
    for y in range(height):
        for x in range(width):
            p = np.array([x, y])

            if point_in_triangle(
            p,
            red_point,
            green_point,
            blue_point
        ):
                d_red = np.linalg.norm(p - red_point)
                d_green = np.linalg.norm(p - green_point)
                d_blue = np.linalg.norm(p - blue_point)

            # Convert distances into "closeness"
                r = 1.0 - d_red / max_dist
                g = 1.0 - d_green / max_dist
                b = 1.0 - d_blue / max_dist

                color = np.array([r, g, b])

            # Normalize so colors remain vivid
                color /= color.max()

                image[y, x] = color
            
            # get coordinate for point
    point = add_point(w1, w2, w3)

            
# Display result
    plt.figure(figsize=(8, 7))
    plt.scatter(point[0], point[1])
    plt.annotate(text = "Physical", xy = (25, green_point[1]))
    plt.annotate(text = "Analytical", xy = (350, red_point[1]))
    plt.annotate(text = "Data-Driven", xy = blue_point)
    plt.annotate(text = "My research project", xy = (point[0], point[1]))
    plt.imshow(image)
    plt.axis("off")
    plt.show()

#plot_triangle()
