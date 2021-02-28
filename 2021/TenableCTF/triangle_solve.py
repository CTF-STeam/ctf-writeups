from math import sqrt

# points is a list of 3D points
# ie: [[2, 9, -15], [0, 33, -20], ...]
def FindLargestTriangleArea(points):
    max_a = 0
    for p in points:
        for q in points:
            for r in points:
                s = calc_area(p, q, r)
                if s > max_a:
                    max_a = s
    return max_a

def calc_area(p, q, r):
    a = (q[0] - p[0])**2 + (q[1] - p[1])**2 + (q[2] - p[2])**2
    b = (r[0] - q[0])**2 + (r[1] - q[1])**2 + (r[2] - q[2])**2
    c = (p[0] - r[0])**2 + (p[1] - r[1])**2 + (p[2] - r[2])**2
    s = (4 * a * b - (c - a - b)**2)/16
    return sqrt(s)

# Reading space delimited points from stdin
# and building list of 3D points
points_data = raw_input()
#points_data = '-21,59,-93 -4,91,-2 1,61,2, 0,44,1'
points = []
for point in points_data.split(' '):
  point_xyz = point.split(',')
  points.append([int(point_xyz[0]), int(point_xyz[1]), int(point_xyz[2])])

# Compute Largest Triangle and Print Area rounded to nearest whole number
area = FindLargestTriangleArea(points)
print(int(round(area)))
