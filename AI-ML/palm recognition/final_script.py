import boto3
import cv2
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

print(1111111111111111111111111111111, datetime.now())

s3 = boto3.client('s3')
bucket_name = 'palm-cash-users-palm-list'

# Load the sample image (from local disk)
sample = cv2.imread("hand1.jpg")
best_score = 0
filename = None
image = None
kp1, kp2, mp = None, None, None
counter = 0

# Initialize SIFT detector
sift = cv2.SIFT.create(nOctaveLayers=3, contrastThreshold=0.03)
keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)

# Function to list files in the S3 bucket
def list_files_in_bucket(bucket_name):
    files = []
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for item in response['Contents']:
            files.append(item['Key'])
    return files

# Function to process each image in the bucket
def process_image(file):
    global best_score, filename, image, kp1, kp2, mp, counter
    
    try:
        # Fetch image from S3
        file_response = s3.get_object(Bucket=bucket_name, Key=file)
        img_data = file_response['Body'].read()

        # Convert the byte data to a NumPy array
        nparr = np.frombuffer(img_data, np.uint8)

        # Decode the image using OpenCV
        palm_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Check if the image was successfully decoded
        if palm_img is None:
            print(f"Failed to decode image: {file}")
            return

        # Convert the image to grayscale (necessary for SIFT)
        palm_img_gray = cv2.cvtColor(palm_img, cv2.COLOR_BGR2GRAY)

        print(counter)
        print("Processing:", file)
        counter += 1

        # Check if keypoints are detected
        keypoints_2, descriptors_2 = sift.detectAndCompute(palm_img_gray, None)
        if len(keypoints_2) == 0 or len(keypoints_1) == 0:
            return  # Skip if no keypoints are detected

        # Use FLANN for matching descriptors
        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)

        # Filter matches based on distance ratio (Lowe's ratio test)
        match_points = [p for p, q in matches if p.distance < 0.1 * q.distance]

        # Compute the best score
        keypoints = min(len(keypoints_1), len(keypoints_2))  # Compare keypoints count
        score = len(match_points) / keypoints * 100
        if score > best_score:
            best_score = score
            filename = file
            image = palm_img
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    except Exception as e:
        print(f"Error processing {file}: {e}")

# Get list of files from S3 bucket
files = list_files_in_bucket(bucket_name)

# Use ThreadPoolExecutor to process images in parallel
with ThreadPoolExecutor() as executor:
    executor.map(process_image, files)

# Print the best match and score
print("Best match:", filename)
print("Score:", best_score)

# Draw matches on the images
if image is not None:
    result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
    result = cv2.resize(result, None, fx=0.5, fy=0.5)

    # Display the result
    cv2.imshow("Result", result)

print(222222222222222222222222222222222222222, datetime.now())
cv2.waitKey(0)
cv2.destroyAllWindows()

