# Offline Navigator

Offline Navigator is a Python-based application designed to simulate and test navigation on a map using A* algorithm for pathfinding. The application uses Pygame for the graphical interface and Matplotlib for visualizing the paths on the map.

## Features

- Load a black-and-white map image and convert it into a binary matrix.
- Select start and end points on the map to find the shortest path using the A* algorithm.
- Visualize the path on the map.
- Save the path with direction changes and followed directions to CSV files.

## Installation

To use the Offline Navigator, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NirGeron/Offline_Navigator.git
   cd Offline_Navigator
   ```

2. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare your map image:**
   - Ensure your map image is in black and white, where the walkable paths are white and obstacles are black.
   - Save the map image in the `files` directory.

2. **Run the main script:**
   ```bash
   python main.py
   ```

3. **Interact with the application:**
   - A window will open displaying the map.
   - Click on the map to select the start and end points.
   - The application will compute the shortest path using the A* algorithm and display it on the map.
   - The directions of the path will be saved in `gps.csv` and `offline.csv`.

## Files

- **main.py**: The main script to run the application.
- **files/map_avi.png**: The example map image used by the application.
- **requirements.txt**: The list of required Python libraries.

## Functionality

### create_matrix_from_image(image_path, matrix_rows, matrix_cols, threshold=0.3)

Converts a black-and-white image into a binary matrix.

- **image_path**: Path to the image file.
- **matrix_rows**: Number of rows in the matrix.
- **matrix_cols**: Number of columns in the matrix.
- **threshold**: Threshold for converting pixels to binary.

### heuristic(a, b)

Calculates the Manhattan distance between two points.

### a_star(matrix, start, goal)

Performs the A* algorithm to find the shortest path from `start` to `goal`.

### get_direction(from_node, to_node)

Determines the direction of movement from one node to another.

### save_path_with_direction_changes(path, filename="gps.csv")

Saves the coordinates where there is a change in direction to a CSV file.

### save_followed_directions(path, filename="offline.csv")

Saves the count and direction of continuous movements to a CSV file.


## Acknowledgements

- Pygame for providing the graphical interface.
- Matplotlib for visualizing the paths.
- The A* algorithm for pathfinding.

---

Feel free to customize this README to better fit your project's specifics and structure.
```

Ensure you adjust the paths, file names, and details as per your actual project structure and requirements.
