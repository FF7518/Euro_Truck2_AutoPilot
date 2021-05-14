# 对当前画面处理，信息提取
import numpy as np
import cv2
import win32gui

from PID import simpleCtrl


class Win32screen:
    def __init__(self):
        self.toplist, self.winlist = [], []

    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    def window(self):
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        truck = [(hwnd, title) for hwnd, title in self.winlist if 'euro truck' in title.lower()]
        truck = truck[0]
        hwnd = truck[0]

        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        return bbox


# 返回mask区域
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


# optimize
def optRoadline(lines, color=(0, 255, 255), thickness=3):
    # if this fails, go with some default line
    try:

        # finds the maximum y value for a lane marker
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []
        for i in lines:
            for ii in i:
                ys += [ii[1], ii[3]]
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        for idx, i in enumerate(lines):
            for xyxy in i:
                # These four lines:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])
                A = np.vstack([x_coords, np.ones(len(x_coords))]).T
                m, b = np.linalg.lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y - b) / m
                x2 = (max_y - b) / m

                line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]

            else:
                found_copy = False

                for other_ms in final_lanes_copy:

                    if not found_copy:
                        if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
                            if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(b) > abs(
                                    final_lanes_copy[other_ms][0][1] * 0.8):
                                final_lanes[other_ms].append([m, b, line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [[m, b, line]]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(np.mean(x1s)), int(np.mean(y1s)), int(np.mean(x2s)), int(np.mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        print(str(e))


# 绘制道路线条
def roadline(img, gray, lines):
    try:
        # 获取概率最高的两条线条和他们的斜率
        l1, l2, k1, k2 = optRoadline(lines)
        print(k1, k2)
        simpleCtrl(k1, k2)

        cv2.line(img, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(img, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)

        for coords in lines:
            coords = coords[0]
            cv2.line(gray, (coords[0], coords[1]),
                     (coords[2], coords[3]),
                     [255, 0, 0], 3)
    except Exception as e:
        print(e)

    return img, gray


# 参数： k1 k2
# PID算法对行进方向进行控制


# 边缘检测
# masked
'''
masked area

    460,420-------------------590,420
     /                            \
    /                              \
5,460-------------------------1020,460
    |                               |
    |                               |
5,720-------------------------1020,720

'''


def convert2gray(img):
    # gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # canny 边缘检测
    gray = cv2.Canny(gray, threshold1=100, threshold2=200)
    # 高斯模糊
    gray = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
    # mask
    vertices = np.array([
        [5, 700],
        [5, 460],
        [460, 420],
        [590, 420],
        [1020, 460],
        [1020, 700],
    ])
    gray = roi(gray, [vertices])
    # 霍夫变换
    lines = cv2.HoughLinesP(gray, rho=1, theta=np.pi / 180, threshold=90,
                            minLineLength=30, maxLineGap=10)
    img, gray = roadline(img, gray, lines)

    return gray, img


if __name__ == '__main__':
    w = Win32screen()
    print(w.window())