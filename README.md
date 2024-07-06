# Offline Navigator

Offline Navigator is a Python-based application designed to simulate and test navigation on a map using A BFS algorithm for pathfinding.
The application uses Pygame for the graphical interface and Matplotlib for visualizing the paths on the map.

## Features

- Load a black-and-white map image and convert it into a binary matrix.
- Select start and end points on the map to find the shortest path using the A* algorithm.
- Visualize the path on the map.
- Save the path with direction changes and followed directions to CSV files
- Parsing the path direction CSV for offline navigator
- 

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
   - open city_path_generator.py and put your map image you want to run.
   - run via terminal "python city_path_generator.py"
   - choose the path by clicking start point and destination
   - ![image](https://github.com/NirGeron/Offline_Navigator/assets/75199660/e621ae66-4652-4304-a8e0-e87d20a80e11)

2. **Interact with the application:**
   - run ui.py
   - A window will open displaying the map with your current location.
   - Click on the map to select the start and end points.
   - The application will compute the shortest path using the BFS algorithm and display it on the map.
   - once you clicked on "p" button on your keyboard the server will down and you will start navigate offline
   - The directions of the path will be saved in `gps.csv` and `offline.csv`.

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
- The BFS algorithm for pathfinding.

---

Feel free to customize this README to better fit your project's specifics and structure.
```

Ensure you adjust the paths, file names, and details as per your actual project structure and requirements.
