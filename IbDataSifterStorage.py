import os
import io
import avro.datafile

import SharedVars
import IbDataSifterClasses
import IbDataSifterGui
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
	SharedVars.LogDateDirectoryPath = SharedVars.InputDirectoryPath + '/' + SelectedDateText
	LogDateFileList = os.listdir(SharedVars.LogDateDirectoryPath)
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
	# Import all the data files for the selected date
	ImportLoggedDataDate(SelectedDateText)
	# Show the date's logged underlying open, high, low, close
	for ImportedFileObject in SharedVars.ImportedDataFileList:
		if ImportedFileObject['FileName'] == 'SPX-Underlying':
			UnderlyingOpen = ImportedFileObject['FileRecordList'][0]['Last']['Price']
			UnderlyingClose = ImportedFileObject['FileRecordList'][-1]['Last']['Price']
			UnderlyingHigh = -1000000.0
			UnderlyingLow = 1000000.0
			for ImportedFileRecord in ImportedFileObject['FileRecordList']:
				RecordPrice = ImportedFileRecord['Last']['Price']
				if RecordPrice > UnderlyingHigh:
					UnderlyingHigh = RecordPrice
				if RecordPrice < UnderlyingLow:
					UnderlyingLow = RecordPrice
	SharedVars.GuiUnderlyingLabel.configure(text='SPX Open: ' + IbDataSifterUtilities.StringFormatDollars(UnderlyingOpen) +
													', High: ' + IbDataSifterUtilities.StringFormatDollars(UnderlyingHigh) +
													', Low: ' + IbDataSifterUtilities.StringFormatDollars(UnderlyingLow) +
													', Close: ' + IbDataSifterUtilities.StringFormatDollars(UnderlyingClose)
													)
	# Show the date's logged option strike price range
	IbDataSifterGui.GuiFillStrikePriceListBox()
	# Show the date's logged option expiration dates
	IbDataSifterGui.GuiFillExpirationDateListBox()

def SelectLogFile(FileName):
	# Distinguish between underlying and option
	Symbol, ExpirationString, Year, Month, Day, Strike, Right = IbDataSifterUtilities.ParseFileName(FileName)
	SharedVars.GuiDevelopmentMessageLabel.configure(text='[' + Symbol + '][' + ExpirationString + '][' + Year + '][' + Month + '][' + Day + '][' + Strike + '][' + Right + ']')

def ImportLoggedDataDate(SelectedDateText):
	ClearImportedDataFileList()
	ImportLoggedDataFile('SPX-Underlying')

def ClearImportedDataFileList():
	# First traverse any existing imported file entries and delete each one's list of file records
	for ImportedFile in SharedVars.ImportedDataFileList:
		ImportedFile['FileRecordList'].clear()
	# Then delete the top level list
	SharedVars.ImportedDataFileList.clear()

def ImportLoggedDataFile(FileName):
	DataFileObject = IbDataSifterClasses.ImportedDataFileClass()
	DataFileObject['FileName'] = FileName
	FileToImport = open(SharedVars.LogDateDirectoryPath + '/' + FileName, 'r')
	LineNumber = 0
	for Line in FileToImport:
		LineNumber += 1
		FileRecordObject = IbDataSifterClasses.LoggedDataRecordClass()
		try:
			TimeStamp, AvroSerializedRecordString = Line.split('---')
			FileRecordObject['TimeStamp'] = TimeStamp
			ByteBufferAvro = io.BytesIO(bytes(AvroSerializedRecordString, 'utf-8'))
			ByteBufferAvro.seek(0)
			reader = avro.datafile.DataFileReader(ByteBufferAvro, avro.io.DatumReader())
			for datum in reader:
				MonitorDataObject = datum
			ByteBufferAvro.close()
			reader.close()
			FileRecordObject['MonitorData'] = MonitorDataObject
		except Exception as e:
			ByteBufferAvro.close()
			reader.close()
			IbDataSifterUtilities.LogError('Exception in DeserializeObect: ' + str(e))
		DataFileObject['FileRecordList'].append(FileRecordObject)

