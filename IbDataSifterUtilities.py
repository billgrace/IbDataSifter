import SharedVars

def LogError(message):
	ErrorTimeStamp = datetime.datetime.now()
	ErrorTimeString = '{0:%A} {0:%B} {0:%d}, {0:%Y} @ {0:%I:%M%p} '.format(ErrorTimeStamp)
	FormattedErrorString = ErrorTimeString + message
	SharedVars.GuiMessageLabel.config(text=FormattedErrorString)
	print(FormattedErrorString)
