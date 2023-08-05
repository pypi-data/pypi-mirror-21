#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ResetInstancePasswordRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'ResetInstancePassword', 'cvm.api.qcloud.com')

	def get_instanceIds(self):
		return self.get_params().get('instanceIds')

	def set_instanceIds(self, instanceIds):
		self.add_param('instanceIds', instanceIds)

	def get_password(self):
		return self.get_params().get('password')

	def set_password(self, password):
		self.add_param('password', password)

