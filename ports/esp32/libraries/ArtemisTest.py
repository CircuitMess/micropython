from Artemis import *
import time

r = const(5)
pos = [128, 128]
vel = [0.0, 0.0]
t = 0
dt = 0

damp = const(0.9)
grav = const(80)


def draw():
	display.fill(Display.Color.Black)
	display.ellipse(int(pos[0] - r), int(pos[1] - r), int(r * 2), int(r * 2), Display.Color.Red, True)

	if dt != 0:
		f = round(1.0 / dt, 1)
		display.text(str(f), 2, 2, Display.Color.Green)

	display.commit()


def update():
	global t, dt, pos, vel
	nt = time.ticks_ms()
	dt = float(nt - t) / 1000.0
	t = nt

	vel[1] += grav * dt

	pos[0] += vel[0] * dt
	pos[1] += vel[1] * dt

	if pos[0] - r * 3 < 0:
		pos[0] = r * 3
		vel[0] = -vel[0] * damp
	elif pos[0] + r > 128:
		pos[0] = 128 - r
		vel[0] = -vel[0] * damp

	if pos[1] - r * 3 < 0:
		pos[1] = r * 3
		vel[1] = -vel[1] * damp
	elif pos[1] + r > 128:
		pos[1] = 128 - r
		vel[1] = -vel[1] * damp

	if pos[1] == 128 - r:
		vel[0] *= (1 - 0.6 * dt)


begin()
draw()

t = time.ticks_ms()

def press_right():
	global vel
	vel[0] += 80

def press_left():
	global vel
	vel[0] -= 80

def press_up():
	global vel
	vel[1] -= 80

def press_down():
	global vel
	vel[1] += 80

buttons.on_press(Buttons.Select, press_up)
buttons.on_press(Buttons.Back, press_down)
buttons.on_press(Buttons.Up, press_left)
buttons.on_press(Buttons.Down, press_right)

while True:
	update()
	draw()
	buttons.scan()
