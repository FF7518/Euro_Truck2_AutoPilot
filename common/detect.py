"""

detect
2021/5/12 17:13

=========================

INTRODUCTIONS
图像检测技术

=========================
"""
import cv2
import numpy as np

from math import sqrt

from config import ScreenConfig, _SCREEN_TOP, _SCREEN_WIDTH, _SCREEN_HEIGHT
from screen import screen_pywin32

DEFAULT_REGION = ScreenConfig.DEFAULT_REGION

# roi 保留区域为图像的下半部分(但是截掉了最底下的一小块干扰比较大的部分)
VERTICES = np.array([
    [0, 3 * (_SCREEN_HEIGHT + _SCREEN_TOP) // 4],
    [0, (_SCREEN_HEIGHT + _SCREEN_TOP) // 2],
    [_SCREEN_WIDTH, (_SCREEN_TOP + _SCREEN_HEIGHT) // 2],
    [_SCREEN_WIDTH, 3 * (_SCREEN_HEIGHT + _SCREEN_TOP) // 4],
    # [(_SCREEN_WIDTH * 2) // 3, 3 * (_SCREEN_HEIGHT + _SCREEN_TOP) // 4],
    # [_SCREEN_WIDTH // 3, 3 * (_SCREEN_HEIGHT + _SCREEN_TOP) // 4],
])


# 返回mask区域
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked, mask


def line_extract(img, vertices=None):
    # gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # canny 边缘检测
    gray = cv2.Canny(gray, threshold1=150, threshold2=250)
    # 高斯模糊
    gray = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
    # mask
    try:
        if vertices is not None:
            vertices = np.array(vertices)
            gray, mask = roi(gray, [vertices])
            cv2.imwrite('./Detect_mask.png', mask)
    except Exception as e:
        print(e)

    # 给图像加上干扰线条
    # cv2.line(img=gray,
    #          pt1=(360, 650),
    #          pt2=(640, 650),
    #          color=[255, 255, 255],
    #          thickness=8)

    # 霍夫变换
    lines = cv2.HoughLinesP(gray, rho=1, theta=np.pi / 180, threshold=90,
                            minLineLength=50, maxLineGap=5)

    # 对线条进行过滤，拟合左右车道
    def lines_filter(img, lines, color=None, thickness=1):
        if color is None:
            color = [0, 0, 255]

        y_min = _SCREEN_HEIGHT // 2
        y_max = _SCREEN_HEIGHT

        # 根据斜率划分左右线条
        left_lines, right_lines = [], []
        for line in lines:
            for x1, y1, x2, y2 in line:
                # y_min = min(y_min, y1)
                # y_min = min(y_min, y2)
                # y_max = max(y_max, y1)
                # y_max = max(y_max, y2)
                k = (y2 - y1) / (x2 - x1)
                length = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
                if length < 50 or abs(k) < 0.1:  # 丢掉长度太小没有参考意义的线条
                    continue
                if k < 0:
                    left_lines.append(line)
                else:
                    right_lines.append(line)
        if len(left_lines) <= 0 or len(right_lines) <= 0:
            return

        # 过滤异常
        drop_lines(left_lines, 0.2)
        drop_lines(right_lines, 0.2)

        # 得到左右车道线点的集合，拟合直线
        left_points = [(x1, y1) for line in left_lines for x1, y1, _, _ in line]
        left_points = left_points + [(x2, y2) for line in left_lines for _, _, x2, y2 in line]
        right_points = [(x1, y1) for line in right_lines for x1, y1, _, _ in line]
        right_points = right_points + [(x2, y2) for line in right_lines for _, _, x2, y2 in line]

        left_line_star = least_squares_fit(left_points, y_min, y_max)
        right_line_start = least_squares_fit(right_points, y_min, y_max)

        return left_line_star, right_line_start

    # 清理异常数据
    def drop_lines(lines, threshold=0.2):
        """
        :param threshold: 差异值大小
        :return:
        """
        # 迭代计算斜率均值，排除掉与差值差异较大的数据
        slope = [(yy2 - yy1) / (xx2 - xx1) for line in lines for xx1, yy1, xx2, yy2 in line]
        while len(lines) > 0:
            mean = np.mean(slope)
            diff = [abs(s - mean) for s in slope]
            idx = np.argmax(diff)
            if diff[idx] > threshold:
                slope.pop(idx)
                lines.pop(idx)
            else:
                break

    # 最小二乘法拟合
    def least_squares_fit(points, ymin, ymax):
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        # polyfit第三个参数为拟合多项式的阶数，所以1代表线性
        fit = np.polyfit(y, x, 1)
        fit_fn = np.poly1d(fit)  # 获取拟合的结果
        xmin = int(fit_fn(ymin))
        xmax = int(fit_fn(ymax))
        return [(xmin, ymin), (xmax, ymax)]



    try:
        left, right = lines_filter(img=img, lines=lines)

        # for line in lines:
        #     for x1, y1, x2, y2 in line:
        #         length = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        #         k = (y2 - y1) / (x2 - x1)
        #
        #         # print((length, k))
        #         cv2.line(img=img,
        #                  pt1=(x1, y1),
        #                  pt2=(x2, y2),
        #                  color=[0, 255, 0],
        #                  thickness=1)

        cv2.line(img=img,
                 pt1=left[0],
                 pt2=left[1],
                 color=[0, 0, 255],
                 thickness=2)
        cv2.line(img=img,
                 pt1=right[0],
                 pt2=right[1],
                 color=[0, 255, 0],
                 thickness=2)
    except Exception as e:
        print(e)

    return img, lines


if __name__ == '__main__':
    while True:
        img = screen_pywin32(region=DEFAULT_REGION)

        gray, _ = line_extract(img, vertices=VERTICES)

        cv2.imshow('Detect window', gray)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
