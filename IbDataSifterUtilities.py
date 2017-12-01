import SharedVars

def ParseFileName(FileName):
	# Parse a filename in the form: <Symbol>-YYYY-MM-DD-SSSS-<right>
	FirstDashIndex = FileName.find('-')
	Symbol = FileName[0:FirstDashIndex]
	if FileName[FirstDashIndex+1:FirstDashIndex+11] == 'Underlying':
		# This is the underlying's file
		ExpirationString = 'Underlying'
		Year = '.'
		Month = '.'
		Day = '.'
		Strike = '.'
		Right = '.'
	else:
		# This is an option file
		ExpirationString = FileName[FirstDashIndex+1:FirstDashIndex+11]
		Year = FileName[FirstDashIndex+1:FirstDashIndex+5]
		Month = FileName[FirstDashIndex+6:FirstDashIndex+8]
		Day = FileName[FirstDashIndex+9:FirstDashIndex+11]
		Strike = FileName[FirstDashIndex+12:FirstDashIndex+16]
		Right = FileName[FirstDashIndex+17:]
	return Symbol, ExpirationString, Year, Month, Day, Strike, Right

def LogError(message):
	ErrorTimeStamp = datetime.datetime.now()
	ErrorTimeString = '{0:%A} {0:%B} {0:%d}, {0:%Y} @ {0:%I:%M%p} '.format(ErrorTimeStamp)
	FormattedErrorString = ErrorTimeString + message
	SharedVars.GuiMessageLabel.config(text=FormattedErrorString)
	print(FormattedErrorString)
