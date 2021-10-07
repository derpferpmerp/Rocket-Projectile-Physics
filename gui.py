from main import create as generate
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import math

plt.style.use("dark_background")
sg.theme('Black')

def radio(lst,kname,size=(20,1)):
	lout = []
	for x in lst:
		lout.append(sg.Radio(
			x,
			kname,
			default=True,
			size=size,
			enable_events=True
		))
	return lout

def slider(bounds,size,default,step,key,label):
	return [
		sg.Text(label, size=(size, 1)),
		sg.Slider(
			(bounds[0], bounds[1]),
			default,
			step,
			orientation="h",
			size=(size, 15),
			key=key,
			enable_events=True
		)
	]
presets = {
	"MASS": 100,
	"GRAV": 9.81,
	"DENS": 1.22541245,
	"DRCF": 0.04,
	"VEL0": 200,
	'BETA': math.radians(10),
}

DEFAULT_ROCKET_AMOUNT = 10

layout = []
for k, v in list(presets.items()):
	layout.append([
		sg.Text(k, size=(20, 1)),
		sg.InputText(v,key=f"-{k} SLIDER-")
	])
layout += [
	[
		sg.Checkbox(
			'Randomizer',
			default=False,
			key="-RAND VAR-",
			enable_events=True
		)
	],
	[
	sg.Text('Amount of Rockets: ', size=(20, 1)),
	sg.Slider(
		(1, 100),
		DEFAULT_ROCKET_AMOUNT,
		1,
		orientation="h",
		size=(20, 15),
		key="-RAMOUNT SLIDER-",
		enable_events=True
    )
	],
	[
	sg.Text('Minimum Velocity: ', size=(20, 1)),
	sg.Slider(
		(5, 100),
		10,
		1,
		orientation="h",
		size=(20, 15),
		key="-VMIN SLIDER-",
		enable_events=True
    )
	],
	[
	sg.Text('Maximum Velocity: ', size=(20, 1)),
	sg.Slider(
		(5, 1100),
		1000,
		1,
		orientation="h",
		size=(20, 15),
		key="-VMAX SLIDER-",
		enable_events=True
    )
	],
	[sg.Button("Generate Simulation")],
	[sg.Button("Exit")]
]

window = sg.Window(
	title="Rocket Physics",
	layout=layout,
	margins=(100, 50)
)
currentbutton = None
hasclickedbutton = False
matplotlibWindowOpen = False
set2rand = False
while True:
	event, values = window.read()
	if not matplotlibWindowOpen and event == sg.WIN_CLOSED:
		break
	elif event == "Generate Simulation":
		if set2rand:
			method="GENERATE"
		else:
			method="PRESET"
		generate(
			MASS=float(values["-MASS SLIDER-"]),
			GRAV=float(values["-GRAV SLIDER-"]),
			DENS=float(values["-DENS SLIDER-"]),
			DRCF=float(values['-DRCF SLIDER-']),
			VEL0=float(values['-VEL0 SLIDER-']),
			n=int(round(float(values['-RAMOUNT SLIDER-']))),
			vb=[
				float(values['-VMIN SLIDER-']),
				float(values['-VMAX SLIDER-'])
			],
			cli=False,
			method=method
		)
		
	elif matplotlibWindowOpen and event == sg.WIN_CLOSED:
		matplotlibWindowOpen = False
	set2rand = values["-RAND VAR-"]

window.close()
