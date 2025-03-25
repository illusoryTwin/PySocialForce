# # import pandas as pd
# # import numpy as np


# # # Load the dataset
# # csv_file = '../data/trajectories_with_velocity.csv'  # Update with actual path
# # df = pd.read_csv(csv_file)


# # # Convert numeric columns
# # df[["X", "Y", "Vx", "Vy"]] = df[["X", "Y", "Vx", "Vy"]].astype(float)

# # # Group data by Track_ID
# # grouped = df.groupby("Track_ID")

# # # Create initial_state list
# # initial_state = []

# # for track_id, group in grouped:
# #     first_entry = group.iloc[0]  # First occurrence of the pedestrian
# #     last_entry = group.iloc[-1]  # Last known position (goal)

# #     # Extract position, velocity, and goal
# #     px, py = first_entry["X"], first_entry["Y"]
# #     vx, vy = first_entry["Vx"], first_entry["Vy"]
# #     gx, gy = last_entry["X"], last_entry["Y"]  # Assuming last known position as goal

# #     initial_state.append([px, py, vx, vy, gx, gy])

# # # Convert to numpy array
# # initial_state = np.array(initial_state)

# # # Display the result
# # print(initial_state.shape)



# # # # # Load the dataset
# # # # df = pd.read_csv(data)

# # # # # Display the first few rows
# # # # print(df.head())



# import pandas as pd
# import numpy as np

# def load_initial_state(csv_file):
#     """
#     Loads pedestrian tracking data and extracts the initial state in the form:
#     (px, py, vx, vy, gx, gy), using:
#       - The **third occurrence** as the initial state.
#       - The **tenth occurrence** as the goal position (or last position if not available).
    
#     Parameters:
#         csv_file (str): Path to the CSV file containing pedestrian trajectory data.
    
#     Returns:
#         np.ndarray: Array of shape (num_pedestrians, 6) with initial positions, velocities, and goals.
#     """
#     # Load the dataset
#     df = pd.read_csv(csv_file)

#     # Convert relevant columns to numeric values
#     df[["X", "Y", "Vx", "Vy"]] = df[["X", "Y", "Vx", "Vy"]].astype(float)

#     # Group data by Track_ID (each pedestrian)
#     grouped = df.groupby("Track_ID")

#     # Create initial_state list
#     initial_state = []

#     for track_id, group in grouped:
#         # Ensure the group has at least 3 entries for initial state
#         if len(group) >= 3:
#             third_entry = group.iloc[2]  # Third occurrence
#         else:
#             third_entry = group.iloc[-1]  # Fallback to last entry if not enough data

#         # Ensure the group has at least 10 entries for goal position
#         if len(group) >= 10:
#             tenth_entry = group.iloc[9]  # Tenth occurrence
#         else:
#             tenth_entry = group.iloc[-1]  # Fallback to last entry if not enough data

#         # Extract position, velocity, and goal
#         px, py = third_entry["X"], third_entry["Y"]
#         vx, vy = third_entry["Vx"], third_entry["Vy"]
#         gx, gy = tenth_entry["X"], tenth_entry["Y"]  # Goal position

#         initial_state.append([px, py, vx, vy, gx, gy])

#     # Convert list to numpy array
#     return np.array(initial_state)


# # Example usage
# csv_file = '../data/trajectories_with_velocity.csv'  # Update with actual path
# initial_state = load_initial_state(csv_file)

# # Display shape & first few entries
# print(f"Shape: {initial_state.shape}")
# print(initial_state[:5])  # Print first 5 rows



import pandas as pd
import numpy as np

def load_initial_state(csv_file):
    """
    Loads pedestrian tracking data and extracts the initial state in the form:
    (Track_ID, px, py, vx, vy, gx, gy), using:
      - The **third occurrence** as the initial state.
      - The **tenth occurrence** as the goal position (or last position if not available).
    
    Parameters:
        csv_file (str): Path to the CSV file containing pedestrian trajectory data.
    
    Returns:
        pd.DataFrame: DataFrame with columns ['Track_ID', 'px', 'py', 'vx', 'vy', 'gx', 'gy']
    """
    # Load the dataset
    df = pd.read_csv(csv_file)

    # Convert relevant columns to numeric values
    df[["X", "Y", "Vx", "Vy"]] = df[["X", "Y", "Vx", "Vy"]].astype(float)

    # Group data by Track_ID (each pedestrian)
    grouped = df.groupby("Track_ID")

    # Create initial_state list
    initial_state = []

    for track_id, group in grouped:
        # Ensure the group has at least 3 entries for initial state
        if len(group) >= 120:
            third_entry = group.iloc[120]  # Third occurrence
        else:
            third_entry = group.iloc[-1]  # Fallback to last entry if not enough data

        # Ensure the group has at least 20 entries for goal position
        if len(group) >= 160:
            tenth_entry = group.iloc[159]  # Tenth occurrence
        else:
            tenth_entry = group.iloc[-1]  # Fallback to last entry if not enough data

        # Extract position, velocity, and goal
        px, py = third_entry["X"], third_entry["Y"]
        vx, vy = third_entry["Vx"], third_entry["Vy"]
        gx, gy = tenth_entry["X"], tenth_entry["Y"]  # Goal position

        # Store Track_ID along with state values
        initial_state.append([track_id, px, py, vx, vy, gx, gy])

    # Convert to DataFrame for better readability
    columns = ["Track_ID", "px", "py", "vx", "vy", "gx", "gy"]
    return pd.DataFrame(initial_state, columns=columns)


# Example usage
csv_file = '../data/trajectories_with_velocity.csv'  # Update with actual path
initial_state_df = load_initial_state(csv_file)

# Display shape & first few rows
print(f"Shape: {initial_state_df.shape}")
print(initial_state_df.head())  # Print first 5 rows
