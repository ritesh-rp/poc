
import os
import cv2
sample = cv2.imread("hand65.jpeg")
best_score = 0
filename = None
image = None
kp1, kp2, mp = None, None, None
counter = 0
sift = cv2.SIFT.create(nOctaveLayers=3, contrastThreshold=0.03)
keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)

for file in os.listdir("hands"):
    print(counter)
    print(file)
    counter += 1

    palm_img = cv2.imread("hands/" + file)
    keypoints_2, descriptors_2 = sift.detectAndCompute(palm_img,None)
    matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10},{}).knnMatch(descriptors_1, descriptors_2, k=2)
    match_points = []
    for p,q in matches:
        if p.distance < 0.1 * q.distance:
            match_points.append(p)
    
    keypoints = 0
    if len(keypoints_1) < len(keypoints_2):
        keypoints = len(keypoints_1)
    else:
        keypoints = len(keypoints_2)
    if len(match_points) / keypoints * 100 > best_score:
        best_score = len(match_points) / keypoints * 100
        filename = file
        image = palm_img
        kp1, kp2, mp = keypoints_1, keypoints_2, match_points

print("Best match: " + filename)
print("Score: " + str(best_score))

result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
result = cv2.resize(result, None, fx=0.5, fy=0.5)

cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()