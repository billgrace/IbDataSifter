import os
import io
import avro.datafile
import avro.io

import SharedVars
import IbDataSifterClasses
import IbDataSifterGui
import IbDataSifterUtilities

def PrepareDataStorage():
	InputDirectoryList = os.listdir(SharedVars.InputDirectoryPath)
	InputDirectoryList.sort()
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
	LogDateFileList.sort(reverse=True)
	# Scan the sorted list of all files and extract items of interest
	SharedVars.LoggedFilesInCurrentDate.clear()
	SharedVars.LoggedStrikePricesInCurrentDate.clear()
	SharedVars.LoggedExpirationDatesInCurrentDate.clear()
	SharedVars.TimestampsInCurrentFile.clear()
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
	ImportLoggedDataDate(SelectedDateText)
	# Show the date's logged underlying open, high, low, close
	UnderlyingIsCached, UnderlyingCacheIndex = FindDataFileInCache('SPX-Underlying')
	UnderlyingCachedFileObject = SharedVars.ImportedDataFileCache[UnderlyingCacheIndex]
	CachedUnderlyingRecordList = UnderlyingCachedFileObject['FileRecordList']
	for Record in CachedUnderlyingRecordList:
		if Record['RecordAppearsValid']:
			UnderlyingOpen = Record['MonitorData']['Last']['Price']
			break;
	UnderlyingClose = CachedUnderlyingRecordList[-1]['MonitorData']['Last']['Price']
	UnderlyingHigh = -1000000.0
	UnderlyingLow = 1000000.0
	SharedVars.ValidRecordIndexesInCurrentFile.clear()
	RecordIndex = -1
	for Record in CachedUnderlyingRecordList:
		RecordIndex += 1
		if Record['RecordAppearsValid'] == True:
			SharedVars.TimestampsInCurrentFile.append(Record['TimeStamp'])
			SharedVars.ValidRecordIndexesInCurrentFile.append(RecordIndex)
			RecordPrice = Record['MonitorData']['Last']['Price']
			if RecordPrice > UnderlyingHigh:
				UnderlyingHigh = RecordPrice
			if RecordPrice < UnderlyingLow:
				UnderlyingLow = RecordPrice
	IbDataSifterGui.GuiShowUnderlyingSummary(UnderlyingOpen, UnderlyingHigh, UnderlyingLow, UnderlyingClose)
	# Show the date's logged option strike price range
	IbDataSifterGui.GuiFillStrikePriceListBox()
	# Show the date's logged option expiration dates
	IbDataSifterGui.GuiFillExpirationDateListBox()
	# # Show the selected file's timestamp list
	# IbDataSifterGui.GuiFillTimestampListBox()

def SelectLogFile(FileName):
	SharedVars.TimestampsInCurrentFile.clear()
	Symbol, ExpirationString, Year, Month, Day, Strike, Right = IbDataSifterUtilities.ParseFileName(FileName)
	IbDataSifterGui.GuiShowDevelopmentMessage('[' + Symbol + '][' + ExpirationString + '][' + Year + '][' + Month + '][' + Day + '][' + Strike + '][' + Right + ']')
	ImportLoggedDataFile(FileName)
	# Show the selected file's timestamp list
	IbDataSifterGui.GuiFillTimestampListBox()

def ImportLoggedDataDate(SelectedDateText):
	ClearImportedDataFileCache()
	IbDataSifterGui.GuiClearUnderlyingSummary()
	# ImportLoggedDataFile('SPX-Underlying')
	SharedVars.GuiLogFilesListBox.select_set(0)
	SelectLogFile('SPX-Underlying')

def ClearImportedDataFileCache():
	# First traverse any existing imported file entries and delete each one's list of file records
	for ImportedFile in SharedVars.ImportedDataFileCache:
		ImportedFile['FileRecordList'].clear()
	# Then delete the top level list
	SharedVars.ImportedDataFileCache.clear()

def FindDataFileInCache(FileName):
	for CacheIndex in range(0, len(SharedVars.ImportedDataFileCache)):
		if SharedVars.ImportedDataFileCache[CacheIndex]['FileName'] == FileName:
			return True, CacheIndex
	return False, 0


def ImportLoggedDataFile(FileName):
	# First check to see if this file is already in our cache
	FileIsCached, CacheIndexOfThisDataFile = FindDataFileInCache(FileName)
	if FileIsCached:
		return CacheIndexOfThisDataFile
	# OK, it's not already in memory cache so import it from storage
	DataFileObject = IbDataSifterClasses.ImportedDataFileClass()
	DataFileObject['FileName'] = FileName
	FileToImportPathName = SharedVars.LogDateDirectoryPath + '/' + FileName
	try:
		FileToImport = open(FileToImportPathName, 'r')
	except Exception as e:
		# for now, just ignore the issue of empty directories
		SharedVars.ImportedDataFileCache.append(DataFileObject)
		return
	SizeOfFileToImport = os.path.getsize(FileToImportPathName)
	CurrentPositionInFileToImport = 0
	LineNumber = 0
	IbDataSifterGui.InitializeProgressBar('Importing ' + FileName)
	for Line in FileToImport:
		CurrentPositionInFileToImport += (len(Line) + 1)
		LineNumber += 1
		IbDataSifterGui.UpdateProgressBar((CurrentPositionInFileToImport/SizeOfFileToImport)*100)
		if LineNumber % 100 == 0:
			IbDataSifterGui.GuiShowDevelopmentMessage('Record ' + str(LineNumber))
			SharedVars.GuiWindow.update()
		FileRecordObject = IbDataSifterClasses.LoggedDataRecordClass()
		MonitorDataObject = IbDataSifterClasses.MonitorDataClass()
		try:
			TimeStampString, AvroStringWithByteTags = Line.split('---')
			TimeStampObject = IbDataSifterClasses.LoggedDataRecordTimeStampClass()
			TimeStampObject['Hour'] = int(TimeStampString[0:2])
			TimeStampObject['Minute'] = int(TimeStampString[3:5])
			TimeStampObject['Second'] = int(TimeStampString[6:8])
			TimeStampObject['Millisecond'] = int(TimeStampString[9:12])
			FileRecordObject['TimeStamp'] = TimeStampObject
			AvroString = AvroStringWithByteTags[2:-2]
			AvroByteArray = IbDataSifterUtilities.DecodeStringToBytes(AvroString)
			AvroByteStream = io.BytesIO(AvroByteArray)
			reader = avro.datafile.DataFileReader(AvroByteStream, avro.io.DatumReader())
			for datum in reader:
				MonitorDataObject = datum
			AvroByteStream.close()
			reader.close()
			FileRecordObject['MonitorData'] = MonitorDataObject
			FileRecordObject['RecordAppearsValid'] = UnderlyingRecordIsValid(MonitorDataObject)
		except Exception as e:
			IbDataSifterUtilities.LogError('Exception in DeserializeObect: ' + str(e))
		DataFileObject['FileRecordList'].append(FileRecordObject)
	IbDataSifterGui.CloseProgressBar()
	FileToImport.close()
	SharedVars.ImportedDataFileCache.append(DataFileObject)
	FileIsCached, CacheIndexOfThisDataFile = FindDataFileInCache(FileName)
	return CacheIndexOfThisDataFile

def UnderlyingRecordIsValid(RecordObject):
	if RecordObject['Last']['Price'] > 0.009:
		return True
	else:
		return False

def OptionRecordIsValid(RecordObject):
	a=1
	return False

