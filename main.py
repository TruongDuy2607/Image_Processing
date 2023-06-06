import cv2
import numpy as np
import matplotlib.pyplot as plt

def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M, N), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            try:
                q = 255
                r = 255

                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j + 1]
                    r = img[i, j - 1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i + 1, j - 1]
                    r = img[i - 1, j + 1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i + 1, j]
                    r = img[i - 1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i - 1, j - 1]
                    r = img[i + 1, j + 1]

                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0

            except IndexError as e:
                pass

    return Z

# Đọc ảnh grayscale
image = cv2.imread("./Image/img.png", cv2.IMREAD_GRAYSCALE)
image = cv2.GaussianBlur(image, (5,5), 0)

# Áp dụng Sobel để tính toán gradient
gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# Tính toán độ lớn và hướng gradient
gradient_magnitude = np.sqrt(np.square(gradient_x) + np.square(gradient_y))
gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
gradient_direction = np.arctan2(gradient_y, gradient_x)

# Loại bỏ các điểm không cực đại

result_image = non_max_suppression(gradient_magnitude, gradient_direction).astype(np.uint8)
# Hiển thị ảnh kết quả sau non-maximum suppression
# cv2.imshow("Non-Maximum Suppression", result_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
fix, axs = plt.subplots(1,2, figsize=(16, 8))
axs[0].imshow(gradient_magnitude, cmap='gray')
axs[0].axis('off')
axs[0].set_title("Sobel Kernal")
axs[1].imshow(result_image, cmap='gray')
axs[1].axis('off')
axs[1].set_title("Sobel Kernal")
plt.show()