import SharedVars

from enum import Enum

class RequestedMonitorStatus(Enum):
	NotSpecified = 0
	Pending = 1
	Active = 2
	RejectedByIB = 3

class ReadRequestResultReturnCode(Enum):
	NotSpecified = 0
	Success = 1
	IdNotOnActiveList = 2

