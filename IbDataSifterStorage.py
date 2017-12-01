import os

import SharedVars
import IbDataSifterGui
import IbDataSifterStorage
import IbDataSifterUtilities

def PrepareDataStorage():
	InputDirectoryList = os.listdir(SharedVars.InputDirectoryPath)
	InputDirectoryList.sort()
	# SharedVars.GuiMessageLabel.configure(text='len(LogDateFileList)' + str(len(InputDirectoryList)))
	for CurrentIndex in range(0, len(InputDirectoryList)-1):
		CurrentDirectory = InputDirectoryList[CurrentIndex]
		if CurrentDirectory[0] != '2':
			del InputDirectoryList[CurrentIndex]
	for EachDirectory in InputDirectoryList:
		SharedVars.TradedDayDirectories.append(EachDirectory)

def ReadPreferencesFile():
	try:
		PreferenceFile = open('Preferences.cfg', 'r')
		LineNumber = 0
		for Line in PreferenceFile:
			LineNumber += 1
			if Line[0] == '#':
				continue
			try:
				UnstrippedKeyWord, UnstrippedKeyValue = Line.split('=')
				KeyWord = UnstrippedKeyWord.strip()
				KeyValue = UnstrippedKeyValue.strip()
				if(KeyWord == 'InputDirectoryPath'):
					SharedVars.InputDirectoryPath = KeyValue
					# print('SharedVars.InputDirectoryPath: ' + str(SharedVars.InputDirectoryPath))
				elif(KeyWord == 'OutputDirectoryPath'):
					SharedVars.OutputDirectoryPath = KeyValue
					# print('SharedVars.OutputDirectoryPath: ' + str(SharedVars.OutputDirectoryPath))
				# elif(KeyWord == 'StatusReportingInterval'):
				# 	SharedVars.StatusReportingInterval = float(KeyValue)
				# 	# print('SharedVars.StatusReportingInterval: ' + str(SharedVars.StatusReportingInterval))
				# elif(KeyWord == 'StrikePriceRange'):
				# 	SharedVars.StrikePriceRange = int(KeyValue)
				# 	# print('SharedVars.StrikePriceRange: ' + str(SharedVars.StrikePriceRange))
				# elif(KeyWord == 'TradingDayStartTime'):
				# 	StartTimeComponents = KeyValue.split(':')
				# 	SharedVars.TradingDayStartTimeHour = int(StartTimeComponents[0])
				# 	SharedVars.TradingDayStartTimeMinute = int(StartTimeComponents[1])
				# 	# print('SharedVars.TradingDayStartTimeHour:Minute- {0:02d}:{1:02d}'.format(SharedVars.TradingDayStartTimeHour, SharedVars.TradingDayStartTimeMinute))
				else:
					IbDataSifterUtilities.LogError('unrecognized preference.cfg KeyWord: ' + KeyWord + ' on line #' + str(LineNumber))
			except Exception as e:
				IbDataSifterUtilities.LogError('problem parsing preference.cfg line #' + str(LineNumber) + ': ' + Line + ', exception: ' + str(e))
	except Exception as e:
		IbDataSifterUtilities.LogError('unable to open Preferences.cfg - ' + str(e))

def SelectLogDate(SelectedDateText):
	# Get the list of all files in the given date's directory
	SharedVars.CurrentlyOpenTradedDayDirectory = SelectedDateText
	LogDateDirectoryPath = SharedVars.InputDirectoryPath + '/' + SelectedDateText
	LogDateFileList = os.listdir(LogDateDirectoryPath)
	LogDateFileList.sort()
	# Scan the sorted list of all files and extract items of interest
	SharedVars.LoggedFilesInCurrentDate.clear()
	SharedVars.LoggedStrikePricesInCurrentDate.clear()
	SharedVars.LoggedExpirationDatesInCurrentDate.clear()
	for EachFile in LogDateFileList:
		# Make a global copy of all the files in the directory
		SharedVars.LoggedFilesInCurrentDate.append(EachFile)
		# Break out the information contained in the file name
		Symbol, ExpirationString, Year, Month, Day, Strike, Right = IbDataSifterUtilities.ParseFileName(EachFile)
		# Skip over the underlying's file and make lists of the option files
		if 'Underlying' == ExpirationString:
			continue
		# Build a global list of the strike prices
		StrikeAlreadyOnList = False
		for ListStrike in SharedVars.LoggedStrikePricesInCurrentDate:
			if ListStrike == Strike:
				StrikeAlreadyOnList = True
				break;
		if not StrikeAlreadyOnList:
			SharedVars.LoggedStrikePricesInCurrentDate.append(Strike)
		SharedVars.LoggedStrikePricesInCurrentDate.sort()
		# Build a global list of the expiration dates
		ExpirationAlreadyOnList = False
		for ListExpiration in SharedVars.LoggedExpirationDatesInCurrentDate:
			if ListExpiration == ExpirationString:
				ExpirationAlreadyOnList = True
				break;
		if not ExpirationAlreadyOnList:
			SharedVars.LoggedExpirationDatesInCurrentDate.append(ExpirationString)
	SharedVars.LoggedStrikePricesInCurrentDate.sort()
	SharedVars.LoggedExpirationDatesInCurrentDate.sort()
	# Show the list of files in this date's directory
	IbDataSifterGui.GuiFillLoggedFilesListBox(SelectedDateText)
	# Show the date's logged underlying open, high, low, close
	# Show the date's logged option strike price range
	IbDataSifterGui.GuiFillStrikePriceListBox()
	# Show the date's logged option expiration dates
	IbDataSifterGui.GuiFillExpirationDateListBox()

def SelectLogFile(FileName):
	# Distinguish between underlying and option
	Symbol, ExpirationString, Year, Month, Day, Strike, Right = IbDataSifterUtilities.ParseFileName(FileName)
	SharedVars.GuiDevelopmentMessageLabel.configure(text='[' + Symbol + '][' + ExpirationString + '][' + Year + '][' + Month + '][' + Day + '][' + Strike + '][' + Right + ']')
