import SharedVars

class ExpirationDateClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['year'] = 1
		self['month'] = 1
		self['day'] = 2016

class OptionCompStructureClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['Price'] = 0.0
		self['Size'] = 0
		self['ImpliedVolatility'] = 0.0
		self['Delta'] = 0.0
		self['Theta'] = 0.0
		self['Gamma'] = 0.0
		self['Vega'] = 0.0

class MonitorDataClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		ed = ExpirationDateClass()
		aoc = OptionCompStructureClass()
		boc = OptionCompStructureClass()
		loc = OptionCompStructureClass()
		moc = OptionCompStructureClass()
		self['MonitorStatus'] = IbDataLoggerEnums.RequestedMonitorStatus['NotSpecified'].name
		self['RequestSuccessCode'] = IbDataLoggerEnums.ReadRequestResultReturnCode['NotSpecified'].name
		self['SequenceNumber'] = 0
		self['MonitorStartMilliseconds'] = 0
		self['MonitorLastUpdateMilliseconds'] = 0
		self['MonitorUpdateCount'] = 0
		self['Symbol'] = ''
		self['ExpirationDate'] = ed
		self['ContractRight'] = ''
		self['StrikePrice'] = 0.0
		self['SubscriptionId'] = 0
		self['Ask'] = aoc
		self['Bid'] = boc
		self['Last'] = loc
		self['Model'] = moc
		self['Volume'] = 0
		self['TimeStamp'] = ''
		self['Open'] = 0.0
		self['High'] = 0.0
		self['Low'] = 0.0
		self['Close'] = 0.0

class LoggedDataRecordTimeStampClass(dict):
	def __init__(self):
		self['Hour'] = 1
		self['Minute'] = 1
		self['Second'] = 1
		self['Millisecond'] = 1

class LoggedDataRecordClass(dict):
	def __init__(self):
		self['TimeStamp'] = LoggedDataRecordTimeStampClass
		self['MonitorData'] = MonitorDataClass

class ImportedDataFileClass(dict):
	def __init__(self):
		self['FileName'] = ''
		self['FileRecordList'] = []