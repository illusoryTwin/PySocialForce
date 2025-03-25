
import pandas as pd
import numpy as np
from pathlib import Path
import numpy as np
import pysocialforce as psf
from pysocialforce import forces
import matplotlib.pyplot as plt

def load_initial_state(csv_file):
    """
    Loads pedestrian tracking data and extracts the initial state in the form:
    (px, py, vx, vy, gx, gy)
    
    Parameters:
        csv_file (str): Path to the CSV file containing pedestrian trajectory data.
    
    Returns:
        np.ndarray: Array of shape (num_pedestrians, 6) with initial positions, velocities, and goals.
    """
    # Load the dataset
    df = pd.read_csv(csv_file)

    # Convert relevant columns to numeric values
    df[["Y", "X",  "Vy", "Vx"]] = df[["X", "Y", "Vx", "Vy"]].astype(float)

    # Group data by Track_ID (each pedestrian)
    grouped = df.groupby("Track_ID")

    # Create initial_state list
    initial_state = []

    for track_id, group in grouped:
        # first_entry = group.iloc[0]  # First occurrence of the pedestrian
        # last_entry = group.iloc[-1]  # Last known position (goal)
        # Ensure the group has at least 3 entries for initial state
        if len(group) >= 5:
            third_entry = group.iloc[5]  # Third occurrence
        else:
            third_entry = group.iloc[-1]  # Fallback to last entry if not enough data

        # Ensure the group has at least 30 entries for goal position
        if len(group) >= 45:
            tenth_entry = group.iloc[45]  # Tenth occurrence
        else:
            tenth_entry = group.iloc[-1]  # Fallback to last entry if not enough data

        # if len(group) >= 5:
        #     third_entry = group.iloc[75]  # Third occurrence
        # else:
        #     third_entry = group.iloc[-1]  # Fallback to last entry if not enough data

        # # Ensure the group has at least 30 entries for goal position
        # if len(group) >= 45:
        #     tenth_entry = group.iloc[95]  # Tenth occurrence
        # else:
        #     tenth_entry = group.iloc[-1]  # Fallback to last entry if not enough data

        # Extract position, velocity, and goal
        px, py = third_entry["X"], third_entry["Y"]
        vx, vy = third_entry["Vx"], third_entry["Vy"]
        gx, gy = tenth_entry["X"], tenth_entry["Y"]  # Assuming last position as goal

        initial_state.append([px, py, vx, vy, gx, gy])

    # Convert list to numpy array
    return np.array(initial_state)


# Example usage
csv_file = '../data/trajectories_with_velocity.csv'  # Update with actual path
initial_state = load_initial_state(csv_file)
print("initial_state", initial_state)

# initial_state = np.array([
#     [231.280522, 440.882634, 101.168710, -14.557617, 617.742052, 422.200819],
#     [677.274247, 313.422534, 75.324040, -3.884973, 687.533692, 323.717553],
#     [1385.385467, 354.192630, -198.305652, -43.009829, 1114.960502, 223.129210],
#     [1568.671161, 534.303265, -112.671541, -114.265101, 1155.403710, 357.997451],
# ])


# # # =================================
# # initial_state = np.array([
# #     [197.57258197, 445.49186333, 10., 0., 1273.01169297, 943.89184191],
# #     [654.22144191, 312.18302997, 10., 0., 1539.70399262, 889.33161294],
# #     [1436.76992933, 373.86042354, 10., 0., 693.49381373, -94.89905564],
# #     [1616.83187, 563.56815806, 10., 0., 800.43060553, -90.40530094]
# # ])

# initial_state = np.array([
#     [231.28052196, 440.88263362, 101.16870973, -14.55761693, 381.82459878, 434.60594093],
#     [677.27424702, 313.42253355, 75.32403991, -3.8849731, 695.32590798, 302.2278403],
#     [1385.38546658, 354.19263015, -198.30565184, -43.00982852, 1246.44693391, 293.50274598],
#     [1568.67116083, 534.30326529, -112.67154091, -114.26510062, 1353.61364093, 463.35462301],
# ])

# # # initial states, each entry is the position, velocity and goal of a pedestrian in the form of (px, py, vx, vy, gx, gy)
# # initial_state = np.array(
# #     [
# #         [0.0, 10, -0.5, -0.5, 0.0, 0.0],
# #         [0.5, 10, -0.5, -0.5, 0.5, 0.0],
# #         [0.0, 0.0, 0.0, 0.5, 1.0, 10.0],
# #         # [1.0, 0.0, 0.0, 0.5, 2.0, 10.0],
# #         # [2.0, 0.0, 0.0, 0.5, 3.0, 10.0],
# #         # [3.0, 0.0, 0.0, 0.5, 4.0, 10.0],
# #     ]
# # )

# social groups informoation is represented as lists of indices of the state array
groups = [[0, 1], [2], [3]] #, [2, 3]]

# list of linear obstacles given in the form of (x_min, x_max, y_min, y_max)
# obs = [[1, 2, 7, 8]]
obs = None
# initiate the simulator,
s = psf.Simulator(
    initial_state,
    groups=groups,
    obstacles=obs,
    config_file=Path(__file__).resolve().parent.joinpath("custom_config.toml"),
)
# update 80 steps
s.step(20)

f = forces.DesiredForce()
f.init(s, s.config)
f.factor = 1.0
print("The force", f.get_force())
print(s, s.config)


forces_array = f.get_force()


# Extract positions
px = initial_state[:, 0]
py = initial_state[:, 1]

# Extract force vectors
fx = forces_array[:, 0]
fy = forces_array[:, 1]

# # Plot the pedestrians
# plt.figure(figsize=(8, 6))
# plt.quiver(px, py, fx, fy, angles='xy', scale_units='xy', scale=1, color='r', label="Forces")

# # Mark initial positions
# plt.scatter(px, py, color='b', label="Initial Positions")

plt.figure(figsize=(12, 12))  # Increase figure size

# Extract position and velocity
px, py, vx, vy = initial_state[:, 0], initial_state[:, 1], initial_state[:, 2], initial_state[:, 3]

# Plot vectors
plt.quiver(px, py, vx, vy, angles="xy", scale_units="xy", scale=1, color="r", label="Velocity")

# Plot initial positions
plt.scatter(px, py, color="b", label="Initial Position", s=50)

# Set axis limits with some padding
x_min, x_max = px.min() - 50, px.max() + 50
y_min, y_max = py.min() - 50, py.max() + 50
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.legend()
plt.title("Pedestrian Initial State with Velocity Vectors")
plt.grid(True)
plt.axis("equal")  # Keep aspect ratio equal
plt.show()

# plt.xlabel("X Position")
# plt.ylabel("Y Position")
# plt.title("Force Vectors Acting on Pedestrians")
# plt.legend()
# plt.grid()
plt.show()

# with psf.plot.SceneVisualizer(s, "../images/my_test_8") as sv:
#     sv.animate()
#     sv.plot()


