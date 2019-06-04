import cv2

img = cv2.imread("results.jpg")

green = (0, 255, 0)
red = (255, 0, 0)
cv2.line(img, (355, 0), (355, 480), green)
cv2.line(img, (285, 0), (285, 480), green)

cv2.line(img, (520, 0), (520, 480), red)
cv2.line(img, (120, 0), (120, 480), red)
cv2.imshow("test", img)

cv2.waitKey(0)
cv2.destroyAllWindows()