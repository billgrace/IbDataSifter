import SharedVars
import IbDataSifterClasses
import IbDataSifterGui
import IbDataSifterStorage
import IbDataSifterClasses

def InitializeEventBindings():
	SharedVars.GuiWindow.bind_all('<Shift-KeyPress-F4>', OnShiftF4KeyPress)

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

def OnShiftF4KeyPress(KeyPressEvent):
	# Shift-F4 => close the application
	SharedVars.GuiWindow.destroy()

def LogError(message):
	ErrorTimeStamp = datetime.datetime.now()
	ErrorTimeString = '{0:%A} {0:%B} {0:%d}, {0:%Y} @ {0:%I:%M%p} '.format(ErrorTimeStamp)
	FormattedErrorString = ErrorTimeString + message
	SharedVars.GuiMessageLabel.config(text=FormattedErrorString)
	print(FormattedErrorString)

def StringFormatDollars(FloatAmount):
	return '${:,.2f}'.format(FloatAmount)

def StringFormatGreek(FloatAmount):
	return '{:,0.4f}'.format(FloatAmount)
