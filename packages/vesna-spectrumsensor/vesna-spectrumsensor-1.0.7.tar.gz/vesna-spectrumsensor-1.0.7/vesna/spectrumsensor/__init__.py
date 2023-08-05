import base64
import re
import select
import serial
import struct

class SpectrumSensorException(Exception): pass

class Device:
	"""A spectrum sensing device.

	A particular hardware model can have one or more physical spectrum sensing devices, each of which
	can support one or more configurations.
	"""
	def __init__(self, id, name):
		"""Create a new device.

		id -- numeric device id, as returned by the "list" command.
		name -- string with a human readable name of the device.
		"""
		self.id = id
		self.name = name
		self.supports_sampling = False

class DeviceConfig:
	"""Configuration for a spectrum sensing device.

	The set of possible configurations for a device is usually hardware-dependent (i.e. a
	configuration usually reflects physical hardware settings) A configuration defines the usable
	frequency range, resolution bandwidth and sweep time for a device.

	By convention, when specifying channel ranges, the range is given in the same format
	as for the range built-in (i.e. inclusive lower bound inclusive, exclusive upper bound).
	When specifiying frequency ranges, both bounds are inclusive.
	"""
	def __init__(self, id, name, device):
		"""Create a new device configuration.

		id -- numeric configuration id, as returned by the "list" command.
		name -- string with a human readable name of the configuration.
		device -- Device object to which this configuration applies.
		"""
		self.id = id
		self.name = name
		self.device = device

	def ch_to_hz(self, ch):
		"""Convert channel number to center frequency in hertz."""
		assert ch >= 0
		assert ch < self.num

		return self.base + self.spacing * ch

	def hz_to_ch(self, hz):
		"""Convert center frequency in hertz to channel number."""
		assert self.covers(hz, hz)

		return int(round((hz - self.base) / self.spacing))

	def get_start_hz(self):
		"""Return the lowest settable frequency."""
		return self.ch_to_hz(0)

	def get_stop_hz(self):
		"""Return the highest settable frequency."""
		return self.ch_to_hz(self.num - 1)

	def covers(self, start_hz, stop_hz):
		"""Return true if this configuration can cover the given frequency band.

		:param start_hz: lower bound of the frequency band to check (inclusive)
		:param stop_hz: upper bound of the frequency band to check (inclusive)
		"""
		return start_hz >= self.get_start_hz() and stop_hz <= self.get_stop_hz()

	def get_full_sweep_config(self, step_hz=None):
		"""Return a sweep configuration that covers the entire frequency range supported
		by this device configuration.

		:param step_hz: frequency step to use (by default, step by a single channel)
		"""

		if step_hz is None:
			step_ch = 1
		else:
			step_ch = max(1, int(round(float(step_hz) / self.spacing)))

		return SweepConfig(self, 0, self.num, step_ch)

	def get_sweep_config(self, start_hz, stop_hz, step_hz):
		"""Return a sweep configuration that covers the specified frequency band.

		:param start_hz: lower bound of the frequency band to sweep (inclusive)
		:param stop_hz: upper bound of the frequency band to sweep (inclusive)
		:param step_hz: sweep frequency step
		"""
		assert self.covers(start_hz, stop_hz)

		# channel start, step, stop as passed to vesna channel config
		# (stop_ch is one past the last channel to be scanned)
		start_ch = self.hz_to_ch(start_hz)
		step_ch = max(1, int(round(step_hz / self.spacing)))
		stop_ch = self.hz_to_ch(stop_hz) + 1

		return SweepConfig(self, start_ch, stop_ch, step_ch)

	def get_sample_config(self, hz, nsamples):
		ch = self.hz_to_ch(hz)

		return SampleConfig(self, ch, nsamples)

	def __str__(self):
		return "channel config %d,%d: %10d - %10d Hz" % (
				self.device.id, self.id, self.get_start_hz(), self.get_stop_hz())

class SweepConfig:
	"""Frequency sweep configuration for a spectrum sensing device.

	:param config: device configuration object to use
	:param start_ch: lowest frequency channel to sweep
	:param stop_ch: one past the highest frequency channel to sweep
	:param step_ch: how many channels in a step
	:param nsamples: how many samples to average per measurement (only supported on some devices)
	"""
	def __init__(self, config, start_ch, stop_ch, step_ch, nsamples=100):
		assert start_ch >= 0
		assert start_ch < config.num
		assert stop_ch >= 0
		assert stop_ch <= config.num
		assert step_ch > 0
		assert nsamples > 0

		self.config = config
		self.start_ch = start_ch
		self.stop_ch = stop_ch
		self.step_ch = step_ch
		self.nsamples = nsamples

		# given (start_ch - stop_ch) range may not be an integer number of step_ch
		last_ch = stop_ch - (stop_ch - start_ch - 1) % step_ch - 1

		# real frequency start, step, stop
		# (stop_hz is the frequency of the last channel)
		self.start_hz = config.ch_to_hz(start_ch)
		self.stop_hz = config.ch_to_hz(last_ch)
		self.step_hz = config.spacing * step_ch

		self.num_channels = len(self.get_ch_list())

	def get_ch_list(self):
		"""Return a list of channels covered by this configuration
		"""
		return list(range(self.start_ch, self.stop_ch, self.step_ch))

	def get_hz_list(self):
		"""Return a list of frequencies covered by this
		configuration
		"""
		return list(map(self.config.ch_to_hz, self.get_ch_list()))

class SampleConfig(SweepConfig):
	"""Frequency sweep configuration for a spectrum sensing device.

	:param config: device configuration object to use
	:param ch: frequency channel to sample
	:param nsamples: number of samples to record
	"""

	def __init__(self, config, ch, nsamples):
		SweepConfig.__init__(self, config, ch, ch+1, 1, nsamples)

class TimestampedData:
	"""Measurement data from a single frequency sweep.

	Attributes:

	timestamp -- Time when the sweep started (in miliseconds since the start of sensing)
	data -- List of measurements, one power measurement in dBm per channel sweeped.
	"""
	def __init__(self):
		self.timestamp = None
		self.channel = None
		self.data = []

Sweep = TimestampedData

class ConfigList:
	"""List of devices and device configurations supported by attached hardware."""

	def __init__(self):
		"""Create a new list."""
		self.configs = []
		self.devices = []

	def _add_device(self, device):
		self.devices.append(device)

	def _add_config(self, config):
		self.configs.append(config)

	def get_config(self, device_id, config_id):
		"""Return the specified device configuration.

		:param device_id: numeric device id, as returned by the `list` command
		:param config_id: numeric configuration id, as returned by the `list` command
		"""
		for config in self.configs:
			if config.id == config_id and config.device.id == device_id:
				return config

		return None

	def get_sweep_config(self, start_hz, stop_hz, step_hz, name=None):
		"""Return best frequency sweep configuration for specified requirements.

		:param start_hz: lower bound of the frequency band to sweep (inclusive)
		:param stop_hz: upper bound of the frequency band to sweep (inclusive)
		:param step_hz: preferred frequency step to use
		:param name: optional required sub-string in device configuration name
		"""

		candidates = []

		for config in self.configs:
			if name and name not in config.name:
				continue

			if not config.covers(start_hz, stop_hz):
				continue

			candidates.append(config)

		# pick fastest matching config
		candidates.sort(key=lambda x:x.time, reverse=True)

		if candidates:
			return candidates[0].get_sweep_config(start_hz, stop_hz, step_hz)
		else:
			return None

	def __str__(self):
		lines = []
		for device in self.devices:
			lines.append("device %d: %s" % (device.id, device.name))
			for config in self.configs:
				if config.device is device:
					lines.append("  channel config %d,%d: %s" % (device.id, config.id, config.name))
					lines.append("    base: %d Hz" % (config.base,))
					lines.append("    spacing: %d Hz" % (config.spacing,))
					lines.append("    bw: %d Hz" % (config.bw,))
					lines.append("    num: %d" % (config.num,))
					lines.append("    time: %d ms" % (config.time,))

		return '\n'.join(lines)

class SpectrumSensorBase(object):

	def __init__(self):
		self._make_base64_lookup()

	def _make_base64_lookup(self):
		self._base64_lookup = {}
		for x in range(4096):
			y = base64.b64encode(b'\x00'+struct.pack(b'>H', x)).decode('ascii')
			assert y[:2] == 'AA'
			y2 = y[2:]

			self._base64_lookup[y2] = float(x)

	def _unser_base64(self, fields):
		if len(fields) != 9:
			raise ValueError
		if fields[8] != 'BE':
			raise ValueError

		scale = float(fields[5])

		sweep = TimestampedData()
		sweep.timestamp = float(fields[1])
		sweep.channel = int(fields[3])

		b64 = fields[7]

		lookup = self._base64_lookup

		assert scale == 1.

		try:
			sweep.data = [
				lookup[b64[n:n+2]]
				for n in range(0, len(b64), 2)
			]
		except KeyError:
			raise ValueError

		return sweep

class SpectrumSensor(SpectrumSensorBase):
	"""Top-level abstraction of the attached spectrum sensing hardware."""

	COMMAND_TIMEOUT = 0.5
	DATA_TIMEOUT = 300

	def __init__(self, device, calibration=True):
		"""Create a new spectrum sensor object.

		device -- path to the character device for the RS232 port with the spectrum sensor.
		"""
		super(SpectrumSensor, self).__init__()

		if '://' in device:
			self.comm = serial.serial_for_url(device, timeout=self.COMMAND_TIMEOUT)
		else:
			self.comm = serial.Serial(device, 576000, timeout=self.COMMAND_TIMEOUT)
		self.calibration = calibration

		self._write("sweep-off\n")
		self._wait_for_ok()
		self._write("sample-off\n")
		self._wait_for_ok()

	def _write(self, msg):
		self.comm.write(msg.encode('ascii'))

	def _readline(self):
		msg = self.comm.readline()
		return msg.decode('ascii')

	def _wait_for_ok(self):
		while True:
			r = self._readline()
			if r == 'ok\n':
				break
			elif r.startswith("error:"):
				raise SpectrumSensorException(r.strip())

	def set_calibration(self, state):
		"""Turn calibration on or off.
		"""
		self.calibration = state
	
	def get_config_list(self):
		"""Query and return the list of supported device configurations."""

		self._write("list\n")

		config_list = ConfigList()

		device = None
		config = None
		while True:
			line = self._readline()
			if not line:
				break

			g = re.match("device ([0-9]+): (.*)", line)
			if g:
				device = Device(int(g.group(1)), g.group(2))
				config_list._add_device(device)
				continue

			g = re.match("  device supports channel sampling", line)
			if g:
				device.supports_sampling = True
				continue

			g = re.match("  channel config ([0-9]+),([0-9]+): (.*)", line)
			if g:
				config = DeviceConfig(int(g.group(2)), g.group(3), device)
				config_list._add_config(config)
				continue

			g = re.match("    ([a-z]+): ([0-9]+)", line)
			if g:
				value = int(g.group(2))
				assert value >= 0
				setattr(config, g.group(1), value)
				continue

		return config_list

	def get_status(self, config):
		"""Query and return the string with device status."""
		sweep_config = SweepConfig(config, 0, 1, 1)
		self._select_sweep_channel(sweep_config)

		self._write("status\n")

		resp = []

		while True:
			line = self._readline()
			if line:
				resp.append(line)
			else:
				break

		return resp

	def get_fw_version(self):
		"""Query and return version of the firmware on VESNA."""
		self._write("version\n")
		resp = self._readline()

		if resp.startswith("error: unknown command:"):
			resp = None
		else:
			resp = resp.strip()

		return resp

	def _select_sweep_channel(self, sweep_config):
		self._write("select channel %d:%d:%d config %d,%d\n" % (
				sweep_config.start_ch, sweep_config.step_ch, sweep_config.stop_ch,
				sweep_config.config.device.id, sweep_config.config.id))
		self._wait_for_ok()

		if not self.calibration:
			self._write("calib-off\n")
			self._wait_for_ok()

		self._write("samples %d\n" % (
				sweep_config.nsamples))
		self._wait_for_ok()

	@classmethod
	def _unser_old(self, fields):
		if fields[-1] != 'DE':
			raise ValueError

		sweep = TimestampedData()

		sweep.timestamp = float(fields[1])
		sweep.channel = int(fields[3])
		sweep.data = list(map(float, fields[5:-1]))

		return sweep

	@classmethod
	def _unser_dec(self, fields):
		if len(fields) < 9:
			raise ValueError
		if fields[-1] != 'DE':
			raise ValueError

		scale = float(fields[5])

		sweep = TimestampedData()
		sweep.timestamp = float(fields[1])
		sweep.channel = int(fields[3])
		sweep.data = list(map(lambda x:float(x)/scale, fields[7:-1]))

		return sweep

	def _iter_timestamps(self, num):
		while True:
			try:
				line = self._readline()
			except select.error:
				break
			except serial.SerialException:
				# this happens when socket is used and ctrl-c is pressed.
				break

			if not line:
				break

			try:
				fields = line.split()
				if len(fields) < 7:
					raise ValueError
				if fields[0] != 'TS':
					raise ValueError
				if fields[2] != 'CH':
					raise ValueError
				if fields[4] == 'DS':
					sweep = self._unser_old(fields)
				elif fields[4] == 'SC':
					if fields[6] == 'DS':
						sweep = self._unser_dec(fields)
					elif fields[6] == 'BS':
						sweep = self._unser_base64(fields)
					else:
						raise ValueError
				else:
					raise ValueError

				if len(sweep.data) != num:
					raise ValueError

			except ValueError:
				print("Ignoring corrupted line: %s" % (line,))
			else:
				yield sweep

	def sample_run(self, sweep_config, cb):
		"""Run the specified frequency sweep.

		sweep_config -- frequency sweep configuration object
		cb -- callback function
		n_average -- number of samples to average

		This function continuously runs the specified frequency sweep on the attached
		hardware.  The provided callback function is called for each completed sweep:

		cb(sweep_config, sweep)

		Where sweep_config is the SweepConfig object provided when calling run() and sweep
		the Sweep object with measured data.
		"""

		self._select_sweep_channel(sweep_config)

		self._write("sample-on\n")

		self.comm.timeout = self.DATA_TIMEOUT

		for samples in self._iter_timestamps(sweep_config.nsamples):
			if not cb(sweep_config, samples):
				break

		self.comm.timeout = self.COMMAND_TIMEOUT

		self._write("sample-off\n")

		self._wait_for_ok()

	def sweep_run(self, sweep_config, cb):
		"""Run the specified frequency sweep.

		sweep_config -- frequency sweep configuration object
		cb -- callback function.

		This function continuously runs the specified frequency sweep on the attached
		hardware.  The provided callback function is called for each completed sweep:

		cb(sweep_config, sweep)

		Where sweep_config is the SweepConfig object provided when calling run() and sweep
		the Sweep object with measured data.
		"""

		self._select_sweep_channel(sweep_config)

		self._write("sweep-on\n")

		self.comm.timeout = self.DATA_TIMEOUT

		for sweep in self._iter_timestamps(sweep_config.num_channels):
			if not cb(sweep_config, sweep):
				break

		self.comm.timeout = self.COMMAND_TIMEOUT

		self._write("sweep-off\n")

		self._wait_for_ok()

	def run(self, sweep_config, cb):
		return self.sweep_run(sweep_config, cb)
