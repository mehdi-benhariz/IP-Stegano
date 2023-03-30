import cv2
import numpy as np
import BitHiding

image1 = cv2.imread("mandril_color.tif", cv2.IMREAD_COLOR)
image2 = cv2.imread("peppers_color.tif", cv2.IMREAD_COLOR)

bitHidingResult = BitHiding.BitHiding(image1, image2, 3)

cv2.imshow("Original 1, Bit Modified 1", np.concatenate(
    [image1, bitHidingResult[0]], axis=1))
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Original 2, Bit Modified, Averaged Bit Modified 2", np.concatenate(
    [image2, bitHidingResult[1], bitHidingResult[2]], axis=1))
cv2.waitKey(0)
cv2.destroyAllWindows()
