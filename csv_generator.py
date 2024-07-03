import csv

# Define the path points (x, y, yaw)
points = []
x = 100
y = 1000
yaw = 0
for i in range(100):
    x += 5
    y += 2
    yaw += 1
    points.append((x, y, yaw))

# CSV file path
csv_file = 'files/points.csv'

# Write points to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['x', 'y', 'yaw'])  # Write header
    writer.writerows(points)

print(f"CSV file '{csv_file}' generated successfully.")
