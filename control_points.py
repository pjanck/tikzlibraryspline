#!/usr/bin/env python
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# Initial code implementation was from 
# https://www.particleincell.com/wp-content/uploads/2012/06/bezier-spline.js

# if cyclic, then
#   a[i] = 1
#   b[i] = 4
#   c[i] = 1
#   alpha = beta = gamma = 1
# else
#   a[i]   = 1 for 0 < i < n-1
#   a[n-1] = 2
#   b[0]   = 2
#   b[i]   = 4 for 0 < i < n-1
#   b[n-1] = 7
#   c[i]   = 1
# Solve Ax = rx, Ay = ry
def solve(rx, ry, cyclic):
    n = len(rx)
    assert n == len(ry)

    x = [-1e9] * n
    y = [-1e9] * n
    z = [-1e9] * n
    bb = [-1e9] * n

    if cyclic:
        # Since alpha = beta = gamma = 1,
        # b[0] = 3 and u[0] = u[n-1] = 1
        bb[0] = 3.0
    else:
        # b[0] = 2
        bb[0] = 2.0
    x[0] = rx[0]
    y[0] = ry[0]
    z[0] = 1
    print("{}: bb={:.5f}, x={:.5f}pt, y={:.5f}pt, z={:.5f}pt".format(0, bb[0], x[0], y[0], z[0]))
    for i in range(1, n-1):
        bb[i] = 4.0 - 1.0/bb[i-1]       # bb[i] =  b[i] - c[i-1]*a[i]/bb[i-1]
        x[i] = rx[i] - x[i-1]/bb[i-1]   #  x[i] = rx[i] - x[i-1]*a[i]/bb[i-1]
        y[i] = ry[i] - y[i-1]/bb[i-1]   #  y[i] = ry[i] - y[i-1]*a[i]/bb[i-1]
        z[i] = 0.0 - z[i-1]/bb[i-1]     #  z[i] =  u[i] - z[i-1]*a[i]/bb[i-1]
        print("{}: bb={:.5f}, x={:.5f}pt, y={:.5f}pt, z={:.5f}pt".format(i, bb[i], x[i], y[i], z[i]))
    if cyclic:
        # b[n-1] = 3, u[n-1] = 1
        an_1 = 1.0
        bn_1 = 3.0
    else:
        # a[n-1] = 2, b[n-1] = 7
        an_1 = 2.0
        bn_1 = 7.0
    bb[n-1] = bn_1 - an_1/bb[n-2]       # bb[n-1] =  b[n-1] - c[n-2]*a[n-1]/bb[n-2]
    x[n-1] = rx[n-1] - an_1*x[n-2]/bb[n-2]   #  x[n-1] = rx[n-1] - x[n-2]*a[n-1]/bb[n-2]
    y[n-1] = ry[n-1] - an_1*y[n-2]/bb[n-2]   #  y[n-1] = ry[n-1] - y[n-2]*a[n-1]/bb[n-2]
    z[n-1] = 1.0 - z[n-2]/bb[n-2]       #  z[n-1] =  u[n-1] - z[n-2]*a[n-1]/bb[n-2]
    print("{}: bb={:.5f}, x={:.5f}pt, y={:.5f}pt, z={:.5f}pt".format(n-1, bb[n-1], x[n-1], y[n-1], z[n-1]))

    x[n-1] = x[n-1]/bb[n-1]             # x[n-1] = x[n-1]/bb[n-1]
    y[n-1] = y[n-1]/bb[n-1]             # y[n-1] = y[n-1]/bb[n-1]
    z[n-1] = z[n-1]/bb[n-1]             # z[n-1] = z[n-1]/bb[n-1]
    print("{}: bb={:.5f}, x={:.5f}pt, y={:.5f}pt, z={:.5f}pt".format(n-1, bb[n-1], x[n-1], y[n-1], z[n-1]))
    for i in range(n-2, -1, -1):
        x[i] = (x[i] - x[i+1])/bb[i]    # x[i] = (x[i] - c[i]*x[i+1])/bb[i]
        y[i] = (y[i] - y[i+1])/bb[i]    # y[i] = (y[i] - c[i]*y[i+1])/bb[i]
        z[i] = (z[i] - z[i+1])/bb[i]    # z[i] = (z[i] - c[i]*z[i+1])/bb[i]
        print("{}: bb={:.5f}, x={:.5f}pt, y={:.5f}pt, z={:.5f}pt".format(i, bb[i], x[i], y[i], z[i]))

    if cyclic:
        d = 1 + z[0] + z[n-1]
        fx = (x[0] + x[n-1])/d
        fy = (y[0] + y[n-1])/d

        for i in range(n):
            x[i] -= fx*z[i]
            y[i] -= fy*z[i]
    return x, y

def spline_through(points, cyclic):
    K = list(map(lambda x: (x[0]*28.45274, x[1]*28.45274), points))
    n = len(points)

    if not cyclic:
        n -= 1

    rx = [0] * n
    ry = [0] * n
    Qx = [0] * n
    Qy = [0] * n

    if cyclic:
        for i in range(n):
            j = (i+1) % n
            rx[i] = 4*K[i][0] + 2*K[j][0]
            ry[i] = 4*K[i][1] + 2*K[j][1]
    else:
        rx[0] = K[0][0] + 2*K[1][0]
        ry[0] = K[0][1] + 2*K[1][1]
        for i in range(1, n-1):
            rx[i] = 4*K[i][0] + 2*K[i+1][0]
            ry[i] = 4*K[i][1] + 2*K[i+1][1]
        rx[n-1] = 8*K[n-1][0] + K[n][0]
        ry[n-1] = 8*K[n-1][1] + K[n][1]

    Px, Py = solve(rx, ry, cyclic)

    for i in range(n-1):
        Qx[i] = 2*K[i+1][0] - Px[i+1]
        Qy[i] = 2*K[i+1][1] - Py[i+1]
    if cyclic:
        Qx[n-1] = 2*K[0][0] - Px[0]
        Qy[n-1] = 2*K[0][1] - Py[0]
    else:
        Qx[n-1] = (K[n][0] + Px[n-1])/2
        Qy[n-1] = (K[n][1] + Py[n-1])/2

    print(r"\draw[blue, ->] ({:.5f}pt,{:.5f}pt)".format(K[0][0], K[0][1]))
    for i in range(n):
        if cyclic:
            j = (i+1) % n
        else:
            j = i + 1
        print(".. controls ({:.5f}pt,{:.5f}pt) and ({:.5f}pt,{:.5f}pt) .. ({:.5f}pt,{:.5f}pt)" \
                .format(Px[i], Py[i],
                        Qx[i], Qy[i],
                        K[j][0], K[j][1]))
    print(";")
    for i in range(n):
        if cyclic:
            j = (i+1) % n
        else:
            j = i + 1
        print(r"\fill[green] ({:.5f}pt,{:.5f}pt) circle (1pt);".format(Px[i], Py[i]))
        print(r"\fill[red]   ({:.5f}pt,{:.5f}pt) circle (1pt);".format(Qx[i], Qy[i]))
        print(r"\draw ({:.5f}pt,{:.5f}pt) -- ({:.5f}pt,{:.5f}pt);".format(K[i][0], K[i][1], Px[i], Py[i]))
        print(r"\draw ({:.5f}pt,{:.5f}pt) -- ({:.5f}pt,{:.5f}pt);".format(K[j][0], K[j][1], Qx[i], Qy[i]))

if __name__ == '__main__':
    points = [
        (0,1),
        (3,1),
        (2,3),
        (1.5,0),
        #(0,1)
    ]
    print("spline_through:")
    spline_through(points, cyclic=False)
    print("\nclosed_spline_through:")
    spline_through(points, cyclic=True)

# vim: set sw=4 sts=4 ts=8 et tw=0:
