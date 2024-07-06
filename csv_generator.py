import csv

# Function to read the existing CSV file and return the lines as a list
def read_csv(file_path):
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            return [row for row in reader]
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

# Function to write the updated lines back to the CSV file
def write_csv(file_path, lines):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID_STEP", "DIRECTION"])  # Write the header
        writer.writerows(lines)

# Function to update the CSV with the new lines from the server
def update_csv(file_path, new_lines):
    # Read the existing lines from the CSV
    existing_lines = read_csv(file_path)

    # Combine existing lines with new lines
    combined_lines = existing_lines + new_lines

    # Keep only the last 29 lines
    updated_lines = combined_lines[-4:]

    # Write the updated lines back to the CSV
    write_csv(file_path, updated_lines)

# Example usage
file_path = 'coordinatesClient.csv'

# First iteration: Simulating receiving 30 new lines from the server
new_lines_from_server_1 = [
    [0, 'right'],
    [1, 'right'],
    [2, 'right'],
    [3, 'right'],
    [4, 'right']

]

# Update the CSV file with the new lines, keeping only the last 29
update_csv(file_path, new_lines_from_server_1[1:])  # Save from 2 to 30

# Read and print the updated CSV to verify the result
updated_csv = read_csv(file_path)
print("Updated CSV content:")
for row in updated_csv:
    print(row)

# Second iteration: Simulating receiving another 30 new lines from the server
new_lines_from_server_2 = [
    [1, 'right'],
    [2, 'right'],
    [3, 'right'],
    [4, 'right'],
    [5, 'right']

]

# Update the CSV file with the new lines, keeping only the last 29
update_csv(file_path, new_lines_from_server_2[1:])  # Save from 3 to 31

# Read and print the updated CSV to verify the result
updated_csv = read_csv(file_path)
print("Updated CSV content:")
for row in updated_csv:
    print(row)