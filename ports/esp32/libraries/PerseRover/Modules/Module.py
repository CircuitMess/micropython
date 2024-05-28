from . import _Modules


class Module:

	def __init__(self):
		self.inited = False

	def _init(self, bus: _Modules.Modules.Side):
		pass

	def _deinit(self):
		pass

	def initialize(self, bus: _Modules.Modules.Side):
		if self.inited:
			return
		self._init(bus)
		self.inited = True

	def deinitialize(self):
		if not self.inited:
			return
		self._deinit()
		self.inited = False
