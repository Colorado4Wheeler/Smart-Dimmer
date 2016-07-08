#! /usr/bin/env python
# -*- coding: utf-8 -*-

import indigo

import os
import sys
import time
import datetime

################################################################################
class Plugin(indigo.PluginBase):
	
	#
	# Init
	#
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = False
		self.devicestates = {}

	#
	# Delete
	#
	def __del__(self):
		indigo.PluginBase.__del__(self)
		
	#
	# Smart Dim (or brighten)
	#
	def smartDimmer (self, pluginAction):
		self.failSafe (pluginAction)
		
		if pluginAction.props['reverse'] == False:
			self.smartDimming (pluginAction)
		else:
			self.roundRobin (pluginAction)
		
	#
	# Failsafe checking
	#
	def failSafe (self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		
		if pluginAction.props['reverse'] == True:
			if str(dev.id) in self.devicestates:
				# We don't need a device state for round robins
				del self.devicestates[str(dev.id)]
		
		# For normal operation make sure if they manually changed brightness that we change the action to match
		if self.devicestates.has_key(str(dev.id)) == True:
			# Make sure the action matches the device state
			if self.devicestates[str(dev.id)] == 'brighten':
				if dev.brightness == 100:
					self.devicestates[str(dev.id)] = 'dim'
			else:
				if dev.brightness == 0:
					self.devicestates[str(dev.id)] = 'brighten'
		
	#
	# Normal smart dimming
	#
	def smartDimming (self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		percentage = int(pluginAction.props['percentage'])
		brightness = dev.brightness
		
		if self.devicestates.has_key(str(dev.id)) == False:		
			if dev.brightness < 100:
				self.devicestates[str(dev.id)] = 'brighten'
			else:
				self.devicestates[str(dev.id)] = 'dim'
			
		if self.devicestates[str(dev.id)] == 'brighten':
			if (dev.brightness + percentage) < 101:
				indigo.dimmer.brighten(dev.id, by=percentage)
				brightness = brightness + percentage
			else:
				indigo.dimmer.brighten(dev.id, by=100-dev.brightness)	
				brightness = 100	
		else:
			if (dev.brightness - percentage) >= 0:
				indigo.dimmer.dim(dev.id, by=percentage)
				brightness = brightness - percentage
			else:
				indigo.dimmer.dim(dev.id, by=dev.brightness)
				brightness = 0
			
		if brightness == 100:
			self.devicestates[str(dev.id)] = 'dim'
			
		if brightness == 0:
			self.devicestates[str(dev.id)] = 'brighten'	
		
	#
	# Round robin dimming
	#
	def roundRobin (self, pluginAction):
		dev = indigo.devices[pluginAction.deviceId]
		percentage = int(pluginAction.props['percentage'])
		brightness = dev.brightness
		
		if brightness == 100:
			# Turn it off, next execution will brighten again
			indigo.dimmer.dim(dev.id, by=dev.brightness)
			return
		
		if (dev.brightness + percentage) < 101:
			indigo.dimmer.brighten(dev.id, by=percentage)
			brightness = brightness + percentage
		else:
			indigo.dimmer.brighten(dev.id, by=100-dev.brightness)	
			brightness = 100
	
	#
	# Plugin startup
	#
	def startup(self):
		self.debugLog(u"Starting Smart Dimmer")
	
	#	
	# Plugin shutdown
	#
	def shutdown(self):
		self.debugLog(u"Smart Dimmer Shut Down")


	#
	# Threading
	#
	def runConcurrentThread(self):
		try:
			while True:
					self.sleep(1)
		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.

	
