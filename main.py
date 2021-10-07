from math import sqrt, radians, cos, exp, atan, ceil, tan
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import PySimpleGUI as sg

plt.style.use("dark_background")

class Rocket(object):
	def __init__(self, **kwargs):
		allowed_keys = set(['MASS','GRAV','DENS','DRCF','VEL0','BETA'])
		presets = {
			"MASS": 100,
			"GRAV": 9.81,
			"DENS": 1.22541245,
			"DRCF": 0.04,
			"VEL0": 200,
			'BETA': radians(10)
		}
		self.__dict__.update((key, presets[key]) for key in allowed_keys)
		self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)
		
		self.a_wing = 1.7 - sqrt((1.45**2)-(1.3**2))*1.3*0.5
		self.numIntegrate = pow(10,100)
		self.j = integrate.quad(lambda x: cos(self.BETA), self.a_wing, self.numIntegrate)[0]
		self.o = self.j / self.numIntegrate
		self.a_proj = (3/4)*(14)*(2*self.o)
		self.v_term = sqrt(2*self.MASS*self.GRAV)/sqrt(self.DENS * self.a_proj * self.DRCF)
		self.tau = self.v_term / self.GRAV
	
		self.y_peak = (-1*self.v_term*self.tau)*np.log(cos(atan(self.VEL0/self.v_term)))
		self.K_CONST = 1/(self.v_term**2)
		self.y0 = 0
	
	def sec(self,x):
		return 1/cos(x)
	
	def f1(self,theta):
		return tan(theta) \
		* self.sec(theta) \
		+ np.log( \
			tan( \
				(theta/2) + (np.pi/4) \
			) \
		)
		
	def Vf(self, theta):
		p1 = self.VEL0*cos(self.BETA)
		p21 = cos(theta)
		p221 = self.K_CONST * (self.VEL0**2) * cos(self.BETA) * cos(self.BETA)
		p222 = self.f1(self.BETA) - self.f1(theta)
		p22 = sqrt(1+(p221*p222))
		p2 = p21 * p22
		return p1/p2
		
	def intf(self,theta):
		return (self.Vf(theta)**2) * tan(theta)
		
	def final(self, t):
		p1 = self.y0
		p21 = (1/self.GRAV)
		l = []
		try:
			l.append(integrate.quad(
				lambda g: self.intf(g),
				self.BETA,
				t
			)[0])
		except:
			return 0
		p22 = l[0]
		p2 = p21*p22
		return p1 - p2
		
	def v_up(self,h):
		vs = self.v_term**2
		p1 = (vs + self.VEL0**2)
		p2 = exp((-2*self.GRAV*h)/(vs))
		p3 = -1*(vs)
		p4 = (p1*p2) + p3
		return (abs(p4)/p4)*sqrt(abs(p4))

	def v_down(self,h):
		vs = self.v_term**2
		p1 = (vs) * exp(((-2*self.GRAV*self.y_peak) - h)/(vs))
		p2 = vs - p1
		return sqrt(p2)
		
	def gen_Graph(self):
		xl = []
		vu = []
		vd = []
		yl = []
		gg = 0
		for x in np.linspace(0,2 * ceil(self.y_peak),1000):
			xl.append(x)
			vu.append(self.v_up(x))
			vd.append(self.v_down(x))
			sg.one_line_progress_meter(
				'Loading',
				gg,
				1000,
				'key',
				'Creating Graph'
			)
			gg += 1
		xl2 = []
		yl2 = []
		lnp = np.linspace(-1,self.BETA,1000)
		for g in range(len(lnp)):
			x=lnp[g]
			sg.one_line_progress_meter('Parsing Part 2', g + 1, len(lnp))
			xl2.append(x)
			yl2.append(self.final(x))
	
		vu = self.VEL0 * (np.array(vu) / max(vu))
		vd = self.v_term * (np.array(vd) / max(vd))
		vd = vd.tolist()[::-1]
	
		return [xl,vu], [xl,vd], [xl2,yl2]

def generateN(
	MASS=100,
	GRAV=9.81,
	DENS=1.22541245,
	DRCF=0.04,
	VEL0=200,
	BETA=radians(10),
	vb=[10,1000],
	n=10,
	cli=True,
	method="GENERATE"):
	fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(30,10))

	ax1.set_title("$V_{up}$",fontsize=50)
	ax1.set_xlabel("Time",fontsize=30)
	ax1.set_ylabel("Velocity",fontsize=30)

	ax2.set_title("$V_{down}$",fontsize=50)
	ax2.set_xlabel("Time",fontsize=30)
	ax2.set_ylabel("Velocity",fontsize=30)

	ax3.set_title("$Position$",fontsize=50)
	ax3.set_xlabel("Time",fontsize=30)
	ax3.set_ylabel("Altitude",fontsize=30)

	axl = [ax1,ax2,ax3]
	gr = Rocket(
		MASS=MASS,
		GRAV=GRAV,
		DENS=DENS,
		DRCF=DRCF,
		VEL0=VEL0,
		BETA=BETA
	)
	grGraph = gr.gen_Graph()
	for x in range(n):
		vel = random.randrange(vb[0],vb[1])
		
		rckt = Rocket(VEL0=vel)
		if method == "GENERATE":
			r = rckt.gen_Graph()
		else:
			r = grGraph
		for i in range(len(axl)):
			axl[i].plot(
				r[i][0],
				r[i][1],
				label=f"$V={round(vel)}$"
			)
	for ax in axl:
		ax.legend()
	if cli:
		plt.savefig("out.png")
	else:
		plt.show(block=False)

def create(MASS=100,GRAV=9.81,DENS=1.22541245,DRCF=0.04,VEL0=200,BETA=radians(10),n=5,vb=[10,1000],method="GENERATE",cli=False):
	if method=="GENERATE":
		generateN(n=n,cli=cli)
	else:
		generateN(
			MASS=MASS,
			GRAV=GRAV,
			DENS=DENS,
			DRCF=DRCF,
			VEL0=VEL0,
			BETA=BETA,
			method="PRESET",
			vb=vb,
			cli=cli
		)
	


#generateN(n=1)