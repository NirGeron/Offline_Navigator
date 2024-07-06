import math


def calculate_distances_and_yaws(points):
    if len(points) < 4:
        raise ValueError("The list must contain at least 5 points.")

    results = []
    for i in range(0, len(points) - 4, 4):
        point1 = points[i]
        point5 = points[i + 4]

        # Calculate the distance between the points
        dx = point5[0] - point1[0]
        dy = point5[1] - point1[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Calculate the yaw (angle in radians)
        yaw = math.degrees(math.atan2(dy, dx))
        results.append((distance, yaw))

    final_results = []
    distance = 0
    current_yaw = results[0][1]
    for i in range(1, len(results) - 1):
        current_range = abs(current_yaw - results[i][1])
        if current_range > 30 and current_range <= 330 and not distance == 0:
            final_results.append((int(distance) * 1.9, (int((current_yaw-45) % 360))))
            current_yaw = results[i][1]
            distance = 0
        else:
            distance += results[i][0]
        if i == len(results) - 2:
            final_results.append((int(distance) * 1.9, (int(((results[i][1])) % 360))))

    filtered_data = [item for item in final_results if item[0] >= 10]
    return filtered_data
