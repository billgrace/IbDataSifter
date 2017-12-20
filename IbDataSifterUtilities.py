import datetime
import SharedVars
import IbDataSifterClasses
import IbDataSifterGui
import IbDataSifterStorage
import IbDataSifterClasses

# Accept a string that was utf-8-encoded from a byte array and return the byte array from which the string was encoded
def DecodeStringToBytes(String):
	ReturnBytes = bytearray()
	DecodeCounter = 0
	DecodeValue = 0
	CharNumber = 0
	CharValue = 0
	try:
		for Char in String:
			CharValue = Char
			CharNumber += 1
			if DecodeCounter == 0:
				# we're not currently in the process of converting 4 chars to a byte
				if Char == '\\':
					# this char is the beginning of a 4-char set
					DecodeCounter = 1
					DecodeValue = 0
				else:
					# this char is just another char so add it to the byte array
					ReturnBytes.append(ord(Char))
			else:
				if DecodeCounter == 1:
					# This is the character following a backslash
					if Char == 'x':
						# it's the x of '\xnn' so ignore it and move on to collect the two hex digits following
						DecodeCounter = 2
					elif Char == 'n':
						# it's the n of a newline ('\n') so declare a byte value of 10 (linefeed)
						ReturnBytes.append(10)
						DecodeCounter = 0
					elif Char == 'r':
						# it's the r of a carriage return ('\r') so declare a byte value of 13 (CR)
						ReturnBytes.append(10)
						DecodeCounter = 0
					elif Char == '\\':
						# it's the second backslash of an escaped backslash character so declare a single backslash byte
						ReturnBytes.append(ord('\\'))
						DecodeCounter = 0
					else:
						#else we got a not-yet-known escaped sequence so
						print('\nGot {0} after a backslash'.format(Char))
						ReturnBytes.append(ord('\\'))
						ReturnBytes.append(ord(Char))
						DecodeCounter = 0
				elif DecodeCounter == 2:
					# this char is the MSB of the encoded value
					DecodeValue = 16 * IntegerHexValue(Char)
					DecodeCounter = 3
				else:
					# this char is the LSB of the encoded value
					DecodeValue += IntegerHexValue(Char)
					ReturnBytes.append(DecodeValue)
					DecodeCounter = 0
	except Exception as e:
		print('Exception in DecodeStringToBytes: CharNumber: {0}, CharValue: {1}, DecodeCounter: {2}, DecodeValue: {3}'.format(CharNumber, CharValue, DecodeCounter, DecodeValue))
	return ReturnBytes

def IntegerHexValue(Char):
	if Char == '0':
		return 0
	elif Char == '1':
		return 1
	elif Char == '2':
		return 2
	elif Char == '3':
		return 3
	elif Char == '4':
		return 4
	elif Char == '5':
		return 5
	elif Char == '6':
		return 6
	elif Char == '7':
		return 7
	elif Char == '8':
		return 8
	elif Char == '9':
		return 9
	elif Char == 'a':
		return 10
	elif Char == 'b':
		return 11
	elif Char == 'c':
		return 12
	elif Char == 'd':
		return 13
	elif Char == 'e':
		return 14
	elif Char == 'f':
		return 15

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
	SharedVars.GuiDevelopmentMessageLabel.config(text=FormattedErrorString)
	print(FormattedErrorString)

def StringFormatDollars(FloatAmount):
	return '${:,.2f}'.format(FloatAmount)

def StringFormatGreek(FloatAmount):
	return '{:,0.4f}'.format(FloatAmount)
