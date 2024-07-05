import math
import time
import os
import sys

# Constants
theta_spacing = 0.07
phi_spacing = 0.02
R1 = 0.5  # Reduced radius
R2 = 1    # Reduced radius
K2 = 5
screen_width = 160
screen_height = 42
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))*0.3

A = 1
B = 1

def render_frame(A, B):
    output = [' '] * (screen_width * screen_height)
    zbuffer = [0] * (screen_width * screen_height)

    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    for theta in [x * theta_spacing for x in range(int(2 * math.pi / theta_spacing))]:
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        for phi in [x * phi_spacing for x in range(int(2 * math.pi / phi_spacing))]:
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            if L > 0:
                if 0 <= xp < screen_width and 0 <= yp < screen_height:
                    idx = xp + screen_width * yp
                    if ooz > zbuffer[idx]:
                        zbuffer[idx] = ooz
                        luminance_index = int(L * 8)
                        output[idx] = ".,-~:;=!*#$@"[luminance_index]

    sys.stdout.write('\033[H')  # Move cursor to home position
    for j in range(screen_height):
        sys.stdout.write(''.join(output[j * screen_width:(j + 1) * screen_width]) + '\n')
    sys.stdout.flush()

def main():
    global A, B
    while True:
        A += 0.04
        B += 0.02
        render_frame(A, B)
        time.sleep(0.01)  # Decreased sleep time for smoother animation

if __name__ == "__main__":
    main()
