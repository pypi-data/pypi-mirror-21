#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateMetricAggerationRequest(Request):

	def __init__(self):
		Request.__init__(self, 'monitor', 'qcloudcliV1', 'CreateMetricAggeration', 'monitor.api.qcloud.com')

	def get_namespace(self):
		return self.get_params().get('namespace')

	def set_namespace(self, namespace):
		self.add_param('namespace', namespace)

	def get_metricName(self):
		return self.get_params().get('metricName')

	def set_metricName(self, metricName):
		self.add_param('metricName', metricName)

	def get_statisticsType(self):
		return self.get_params().get('statisticsType')

	def set_statisticsType(self, statisticsType):
		self.add_param('statisticsType', statisticsType)

	def get_dimensionNames(self):
		return self.get_params().get('dimensionNames')

	def set_dimensionNames(self, dimensionNames):
		self.add_param('dimensionNames', dimensionNames)

