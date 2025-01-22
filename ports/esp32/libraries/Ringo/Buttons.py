from CircuitOS import Input
from CircuitOS import ADS1015, PCA95XX
from .Pins import *
from machine import Pin


class ButtonInput(Input):
	expander_btns = [
		Buttons.Num_1,
		Buttons.Num_2,
		Buttons.Num_3,
		Buttons.Num_4,
		Buttons.Num_5,
		Buttons.Num_6,
		Buttons.Num_7,
		Buttons.Num_8,
		Buttons.Num_9,
		Buttons.Num_0,
		Buttons.Num_Ast,
		Buttons.Num_Hash,
		Buttons.Home,
		Buttons.Power,
		Buttons.Alt_L,
		Buttons.Alt_R
	]

	ads_btns = [
		Buttons.A,
		Buttons.B
	]

	def __init__(self, expander: PCA95XX, ads: ADS1015):
		super().__init__(len(Buttons.Pins))
		self.expander = expander
		self.ads = ads

		for btn in self.expander_btns:
			self.expander.pin_mode(Buttons.Pins[btn], Pin.IN)

	def expander_scan(self):
		state = self.expander.state_read()

		for exp_btn in self.expander_btns:
			pin = Buttons.Pins[exp_btn]

			released: bool = ((state >> pin) & 1) == 1
			if pin == 14:
				released = not released

			if released:
				self.released(exp_btn)
			else:
				self.pressed(exp_btn)

	def ads_scan(self):
		for btn in self.ads_btns:
			self.ads.read(Buttons.Pins[btn])
			if self.ads.read(Buttons.Pins[btn]) < 5:
				self.pressed(btn)
			else:
				self.released(btn)

	def scan(self):
		self.expander_scan()
		self.ads_scan()
