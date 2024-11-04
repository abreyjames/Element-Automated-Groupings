import math


class Node:
    """
    Represents a 3D point in space with a unique identifier and coordinates.

    Attributes:
        id (str): Unique identifier for the node.
        x (float): X-coordinate of the node in 3D space.
        y (float): Y-coordinate of the node in 3D space.
        z (float): Z-coordinate of the node in 3D space.
    """

    def __init__(self, id: str, x: float, y: float, z: float):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Node(id='{self.id}', x={self.x}, y={self.y}, z={self.z})"


class Line:
    """
    Represents a line segment defined by two nodes in 3D space.

    Attributes:
        id (str): Unique identifier for the line.
        start_node (Node): Node object representing the starting point of the line.
        end_node (Node): Node object representing the ending point of the line.
    """

    def __init__(self, id: str, start_node: Node, end_node: Node):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node

    def __repr__(self):
        return f"Line(id='{self.id}', start_node={self.start_node}, end_node={self.end_node})"


def classify_line_orientation(line):
    """
    Classifies a line as vertical, horizontal, or diagonal based on the 
    angle between its start and end nodes in 3D space.

    Parameters:
        line (Line): The line object to classify.

    Returns:
        str: 'Vertical' if the line has no change in x or y,
             'Horizontal' if the angle is below 10 degrees,
             'Diagonal' if the angle is between 10 and 80 degrees.
    """

    # Calculate differences in coordinates between start and end nodes
    dx = line.end_node.x - line.start_node.x
    dy = line.end_node.y - line.start_node.y
    dz = line.end_node.z - line.start_node.z

    # Check for vertical line (no change in x or y)
    if dx == 0 and dy == 0:
        return 'Vertical'

    # Calculate the angle in degrees between the line and the horizontal plane (xy-plane)
    horizontal_distance = math.sqrt(dx**2 + dy**2)
    angle = math.degrees(math.atan2(dz, horizontal_distance))
    print("the member angle is ", angle)

    # Classify based on the angle
    if abs(angle) < 10:
        return 'Horizontal'
    elif 10 <= abs(angle) <= 80:
        return 'Diagonal'
    else:
        return 'Vertical'  # Covers cases where the angle is above 80 degrees


def calculate_line_midpoint(line):
    """
    Calculates the midpoint of a given line segment in 3D space.

    Parameters:
        line (Line): The line object for which to calculate the midpoint.

    Returns:
        tuple: The (x, y, z) coordinates of the midpoint.
    """
    mid_x = (line.start_node.x + line.end_node.x) / 2
    mid_y = (line.start_node.y + line.end_node.y) / 2
    mid_z = (line.start_node.z + line.end_node.z) / 2
    return mid_x, mid_y, mid_z


def calculate_overall_midpoint(lines):
    """
    Calculates the overall midpoint for a list of lines by averaging their midpoints.

    Parameters:
        lines (list of Line): A list of Line objects.

    Returns:
        tuple: The (x, y, z) coordinates of the overall midpoint.
    """
    if not lines:
        return None  # Return None if the list is empty

    total_x, total_y, total_z = 0.0, 0.0, 0.0

    for line in lines:
        mid_x, mid_y, mid_z = calculate_line_midpoint(line)
        total_x += mid_x
        total_y += mid_y
        total_z += mid_z

    # Average each coordinate by the number of lines
    count = len(lines)
    overall_mid_x = total_x / count
    overall_mid_y = total_y / count
    overall_mid_z = total_z / count

    return overall_mid_x, overall_mid_y, overall_mid_z


def is_line_above_overall_midpoint(line, lines):
    """
    Determines if the midpoint of a given line is above the overall midpoint of all lines.

    Parameters:
        line (Line): The line to check.
        lines (list of Line): The list of all lines for calculating the overall midpoint.

    Returns:
        bool: True if the line's midpoint is above the overall midpoint, False otherwise.
    """
    # Calculate the overall midpoint of all lines
    overall_midpoint = calculate_overall_midpoint(lines)
    if overall_midpoint is None:
        raise ValueError(
            "The list of lines is empty, so the overall midpoint cannot be calculated.")

    # Calculate the midpoint of the given line
    line_mid_x, line_mid_y, line_mid_z = calculate_line_midpoint(line)

    # Compare the z-coordinates of the line's midpoint and the overall midpoint
    return line_mid_z > overall_midpoint[2]  # True if above, False otherwise


# Define nodes and a line
node_start = Node(id='N1', x=0, y=0, z=0)
node_end = Node(id='N2', x=0, y=10, z=0)
line = Line(id='L1', start_node=node_start, end_node=node_end)

# Classify line orientation
result = classify_line_orientation(line)
print(result)  # Outputs: 'Vertical'
