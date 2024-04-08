import numpy as np
import cv2
from scipy.interpolate import interp1d
from scipy.spatial.distance import cdist

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Unable to read image at {image_path}. Check the file path and integrity.")
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    _, thresholded = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresholded

def find_largest_contour(thresholded_image):
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No contours found in the image.")
    largest_contour = max(contours, key=cv2.contourArea)
    return largest_contour[:, 0, :]

def fit_curve_to_path(path_points, kind='cubic'):
    if len(path_points) < 4:
        kind = 'linear'  # Fallback to linear if not enough points for cubic

    # Sort points based on x coordinate to prepare for interpolation
    sorted_points = path_points[np.argsort(path_points[:, 1])]
    x, y = sorted_points[:, 1], sorted_points[:, 0]
    
    # Ensure uniqueness in x to avoid interpolation errors
    unique_x, indices = np.unique(x, return_index=True)
    unique_y = np.array([y[index] for index in indices])

    curve = interp1d(unique_x, unique_y, kind=kind, fill_value='extrapolate')
    return curve

def calculate_perpendicular_distances(actual_path_curve, optimal_path_points):
    # Generate points along the curve
    x_values = np.linspace(optimal_path_points[:, 1].min(), optimal_path_points[:, 1].max(), 500)
    curve_y_values = actual_path_curve(x_values)

    # Create a set of points along the curve
    curve_points = np.column_stack((curve_y_values, x_values))

    # Calculate perpendicular distances from each actual point to the curve
    distances = cdist(optimal_path_points, curve_points, metric='euclidean').min(axis=1)
    return distances

def calculate_standard_deviation(actual_path, optimal_path):
    actual_thresholded = preprocess_image(actual_path)
    optimal_thresholded = preprocess_image(optimal_path)

    actual_contour_points = find_largest_contour(actual_thresholded)
    optimal_contour_points = find_largest_contour(optimal_thresholded)

    optimal_curve = fit_curve_to_path(optimal_contour_points, kind='cubic')
    perpendicular_distances = calculate_perpendicular_distances(optimal_curve, actual_contour_points)

    std_deviation = np.std(perpendicular_distances)
    return std_deviation

# testing- dummy files
# actual_path = 'barbellyour.jpeg'
# optimal_path = 'barbell1.jpeg'
# try:
#     std_deviation = calculate_standard_deviation(actual_path, optimal_path)
#     print(f'Standard Deviation: {std_deviation}')
# except FileNotFoundError as e:
#     print(f'File error: {e}')
# except ValueError as e:
#     print(f'Value error: {e}')

# # testing- dummy files
# actual_path = 'barbellyour.jpeg'
# optimal_path = 'barbell1.jpeg'
# # std_deviation = calculate_standard_deviation(actual_path, optimal_path)
# # print(f'Standard Deviation: {std_deviation}')
