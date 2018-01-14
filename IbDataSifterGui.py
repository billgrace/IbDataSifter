import time
import tkinter
from tkinter import ttk

import IbDataSifter
import IbDataSifterClasses
import IbDataSifterStorage
import IbDataSifterUtilities
import SharedVars

def PrepareGui():
	GuiMainWindowBackgroundColor = 'magenta'
	SharedVars.GuiWindow.geometry(str(SharedVars.GuiMainWindowWidth) + 'x' + str(SharedVars.GuiMainWindowHeight) + '+' + str(SharedVars.GuiMainWindowLeft) + '+' + str(SharedVars.GuiMainWindowTop))
	SharedVars.GuiWindow.configure(background=GuiMainWindowBackgroundColor)
	SharedVars.GuiWindow.resizable(True, True)

	# Paths
	SharedVars.GuiInputPathLabel.place(anchor='nw', relx=SharedVars.GuiInputPathLabelLeftX,rely=SharedVars.GuiInputPathLabelTopY)
	SharedVars.GuiOutputPathLabel.place(anchor='nw', relx=SharedVars.GuiOutputPathLabelLeftX,rely=SharedVars.GuiOutputPathLabelTopY)

	# Logged data date list
	SharedVars.GuiLogDateListBoxLabel.place(anchor='nw', relx=SharedVars.GuiLogDateListBoxLabelLeftX,rely=SharedVars.GuiLogDateListBoxLabelTopY)
	SharedVars.GuiLogDateListBox.place(anchor='nw', relx=SharedVars.GuiLogDateListBoxLeftX,rely=SharedVars.GuiLogDateListBoxTopY)
	SharedVars.GuiLogDateListBox.configure(width=SharedVars.GuiLogDateListBoxWidth, height=SharedVars.GuiLogDateListBoxHeight)
	SharedVars.GuiLogDateListBox.bind('<<ListboxSelect>>', GuiLogDateListBoxCallback)
	for date in SharedVars.TradedDayDirectories:
		SharedVars.GuiLogDateListBox.insert(tkinter.END, date)

	# Logged data file list
	SharedVars.GuiLogFilesListBoxLabel.place(anchor='nw', relx=SharedVars.GuiLogFilesListBoxLabelLeftX,rely=SharedVars.GuiLogFilesListBoxLabelTopY)
	SharedVars.GuiLogFilesListBox.place(anchor='nw', relx=SharedVars.GuiLogFilesListBoxLeftX, rely=SharedVars.GuiLogFilesListBoxTopY)
	SharedVars.GuiLogFilesListBox.configure(width=SharedVars.GuiLogFilesListBoxWidth,height=SharedVars.GuiLogFilesListBoxHeight)
	SharedVars.GuiLogFilesListBox.bind('<<ListboxSelect>>', GuiLoggedFilesListBoxCallback)

	# Strike price list
	SharedVars.GuiStrikePriceListBoxLabel.place(anchor='nw', relx=SharedVars.GuiStrikePriceListBoxLabelLeftX,rely=SharedVars.GuiStrikePriceListBoxLabelTopY)
	SharedVars.GuiStrikePriceListBox.place(anchor='nw', relx=SharedVars.GuiStrikePriceListBoxLeftX,rely=SharedVars.GuiStrikePriceListBoxTopY)
	SharedVars.GuiStrikePriceListBox.configure(width=SharedVars.GuiStrikePriceListBoxWidth, height=SharedVars.GuiStrikePriceListBoxHeight, background='Gray')

	# Expiration date list
	SharedVars.GuiExpirationDateListBoxLabel.place(anchor='nw', relx=SharedVars.GuiExpirationDateListBoxLabelLeftX,rely=SharedVars.GuiExpirationDateListBoxLabelTopY)
	SharedVars.GuiExpirationDateListBox.place(anchor='nw', relx=SharedVars.GuiExpirationDateListBoxLeftX,rely=SharedVars.GuiExpirationDateListBoxTopY)
	SharedVars.GuiExpirationDateListBox.configure(width=SharedVars.GuiExpirationDateListBoxWidth, height=SharedVars.GuiExpirationDateListBoxHeight, background='Gray')

	# Progress bar
	SharedVars.GuiProgressBarLabel.place(anchor='nw', relx=SharedVars.GuiProgressBarLabelLeftX,rely=SharedVars.GuiProgressBarLabelTopY)
	SharedVars.GuiProgressBar.place(anchor='nw', relx=SharedVars.GuiProgressBarLeftX,rely=SharedVars.GuiProgressBarTopY)
	
	# Underlying summary
	SharedVars.GuiUnderlyingLabel.place(anchor='nw', relx=SharedVars.GuiUnderlyingSummaryLeftX,rely=SharedVars.GuiUnderlyingSummaryTopY)
	GuiShowUnderlyingSummary(0, -1, 1, 0)

	# Timestamp list
	SharedVars.GuiTimestampListBoxLabel.place(anchor='nw', relx=SharedVars.GuiTimestampListBoxLabelLeftX, rely=SharedVars.GuiTimestampListBoxLabelTopY)
	SharedVars.GuiTimestampListBox.place(anchor='nw', relx=SharedVars.GuiTimestampListBoxLeftX, rely=SharedVars.GuiTimestampListBoxTopY)
	SharedVars.GuiTimestampListBox.configure(width=SharedVars.GuiTimestampListBoxWidth, height=SharedVars.GuiTimestampListBoxHeight)
	SharedVars.GuiTimestampListBox.bind('<<ListboxSelect>>', GuiTimestampListBoxCallBack)

	# File record display
	SharedVars.GuiFrdFilenameDisplay.place(anchor='nw', relx=SharedVars.GuiFrdFilenameDisplayLeftX, rely=SharedVars.GuiFrdFilenameDisplayTopY)
	SharedVars.GuiFrdRecordTimestampDisplay.place(anchor='nw', relx=SharedVars.GuiFrdRecordTimestampLeftX, rely=SharedVars.GuiFrdRecordTimestampTopY)
	SharedVars.GuiFrdPriceLabel.place(anchor='nw', relx=SharedVars.GuiFrdPriceLeftX, rely=SharedVars.GuiFrdGreekLabelTopY)
	SharedVars.GuiFrdPriceLabel.configure(text='Price')
	SharedVars.GuiFrdSizeLabel.place(anchor='nw', relx=SharedVars.GuiFrdSizeLeftX, rely=SharedVars.GuiFrdGreekLabelTopY)
	SharedVars.GuiFrdSizeLabel.configure(text='Size')
	SharedVars.GuiFrdImpliedVolatilityLabel.place(anchor='nw', relx=SharedVars.GuiFrdImpliedVolatilityLeftX, rely=SharedVars.GuiFrdGreekLabelTopY)
	SharedVars.GuiFrdImpliedVolatilityLabel.configure(text='ImpVol')
	SharedVars.GuiFrdDeltaLabel.place(anchor='nw', relx=SharedVars.GuiFrdDeltaLeftX, rely=SharedVars.GuiFrdGreekLabelTopY)
	SharedVars.GuiFrdDeltaLabel.configure(text='Delta')
	SharedVars.GuiFrdThetaLabel.place(anchor='nw', relx=SharedVars.GuiFrdThetaLeftX, rely=SharedVars.GuiFrdGreekLabelTopY)
	SharedVars.GuiFrdThetaLabel.configure(text='Theta')
	SharedVars.GuiFrdGammaLabel.place(anchor='nw', relx=SharedVars.GuiFrdGammaLeftX, rely=SharedVars.GuiFrdGreekLabelTopY)
	SharedVars.GuiFrdGammaLabel.configure(text='Gamma')
	SharedVars.GuiFrdVegaLabel.place(anchor='nw', relx=SharedVars.GuiFrdVegaLeftX, rely=SharedVars.GuiFrdGreekLabelTopY)
	SharedVars.GuiFrdVegaLabel.configure(text='Vega')
	SharedVars.GuiFrdAskLabel.place(anchor='ne', relx=SharedVars.GuiFrdABLMLabelRightX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdAskLabel.configure(text='Ask')
	SharedVars.GuiFrdBidLabel.place(anchor='ne', relx=SharedVars.GuiFrdABLMLabelRightX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdBidLabel.configure(text='Bid')
	SharedVars.GuiFrdLastLabel.place(anchor='ne', relx=SharedVars.GuiFrdABLMLabelRightX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdLastLabel.configure(text='Last')
	SharedVars.GuiFrdModelLabel.place(anchor='ne', relx=SharedVars.GuiFrdABLMLabelRightX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdModelLabel.configure(text='Model')
	SharedVars.GuiFrdOpenLabel.place(anchor='ne', relx=SharedVars.GuiFrdOtherLabelRightX, rely=SharedVars.GuiFrdOpenTopY)
	SharedVars.GuiFrdOpenLabel.configure(text='Open')
	SharedVars.GuiFrdHighLabel.place(anchor='ne', relx=SharedVars.GuiFrdOtherLabelRightX, rely=SharedVars.GuiFrdHighTopY)
	SharedVars.GuiFrdHighLabel.configure(text='High')
	SharedVars.GuiFrdLowLabel.place(anchor='ne', relx=SharedVars.GuiFrdOtherLabelRightX, rely=SharedVars.GuiFrdLowTopY)
	SharedVars.GuiFrdLowLabel.configure(text='Low')
	SharedVars.GuiFrdCloseLabel.place(anchor='ne', relx=SharedVars.GuiFrdOtherLabelRightX, rely=SharedVars.GuiFrdCloseTopY)
	SharedVars.GuiFrdCloseLabel.configure(text='Close')
	SharedVars.GuiFrdVolumeLabel.place(anchor='ne', relx=SharedVars.GuiFrdOtherLabelRightX, rely=SharedVars.GuiFrdVolumeTopY)
	SharedVars.GuiFrdVolumeLabel.configure(text='Volume')
	SharedVars.GuiFrdTimeStampLabel.place(anchor='ne', relx=SharedVars.GuiFrdOtherLabelRightX, rely=SharedVars.GuiFrdTimeStampTopY)
	SharedVars.GuiFrdTimeStampLabel.configure(text='IB TimeStamp')

	SharedVars.GuiFrdAskPriceDisplay.place(anchor='nw', relx=SharedVars.GuiFrdPriceLeftX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdAskSizeDisplay.place(anchor='nw', relx=SharedVars.GuiFrdSizeLeftX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdAskImpliedVolatilityDisplay.place(anchor='nw', relx=SharedVars.GuiFrdImpliedVolatilityLeftX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdAskDeltaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdDeltaLeftX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdAskThetaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdThetaLeftX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdAskGammaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdGammaLeftX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdAskVegaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdVegaLeftX, rely=SharedVars.GuiFrdAskTopY)
	SharedVars.GuiFrdBidPriceDisplay.place(anchor='nw', relx=SharedVars.GuiFrdPriceLeftX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdBidSizeDisplay.place(anchor='nw', relx=SharedVars.GuiFrdSizeLeftX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdBidImpliedVolatilityDisplay.place(anchor='nw', relx=SharedVars.GuiFrdImpliedVolatilityLeftX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdBidDeltaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdDeltaLeftX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdBidThetaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdThetaLeftX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdBidGammaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdGammaLeftX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdBidVegaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdVegaLeftX, rely=SharedVars.GuiFrdBidTopY)
	SharedVars.GuiFrdLastPriceDisplay.place(anchor='nw', relx=SharedVars.GuiFrdPriceLeftX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdLastSizeDisplay.place(anchor='nw', relx=SharedVars.GuiFrdSizeLeftX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdLastImpliedVolatilityDisplay.place(anchor='nw', relx=SharedVars.GuiFrdImpliedVolatilityLeftX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdLastDeltaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdDeltaLeftX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdLastThetaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdThetaLeftX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdLastGammaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdGammaLeftX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdLastVegaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdVegaLeftX, rely=SharedVars.GuiFrdLastTopY)
	SharedVars.GuiFrdModelPriceDisplay.place(anchor='nw', relx=SharedVars.GuiFrdPriceLeftX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdModelSizeDisplay.place(anchor='nw', relx=SharedVars.GuiFrdSizeLeftX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdModelImpliedVolatilityDisplay.place(anchor='nw', relx=SharedVars.GuiFrdImpliedVolatilityLeftX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdModelDeltaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdDeltaLeftX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdModelThetaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdThetaLeftX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdModelGammaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdGammaLeftX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdModelVegaDisplay.place(anchor='nw', relx=SharedVars.GuiFrdVegaLeftX, rely=SharedVars.GuiFrdModelTopY)
	SharedVars.GuiFrdOpenDisplay.place(anchor='nw', relx=SharedVars.GuiFrdOtherLeftX, rely=SharedVars.GuiFrdOpenTopY)
	SharedVars.GuiFrdHighDisplay.place(anchor='nw', relx=SharedVars.GuiFrdOtherLeftX, rely=SharedVars.GuiFrdHighTopY)
	SharedVars.GuiFrdLowDisplay.place(anchor='nw', relx=SharedVars.GuiFrdOtherLeftX, rely=SharedVars.GuiFrdLowTopY)
	SharedVars.GuiFrdCloseDisplay.place(anchor='nw', relx=SharedVars.GuiFrdOtherLeftX, rely=SharedVars.GuiFrdCloseTopY)
	SharedVars.GuiFrdVolumeDisplay.place(anchor='nw', relx=SharedVars.GuiFrdOtherLeftX, rely=SharedVars.GuiFrdVolumeTopY)
	SharedVars.GuiFrdTimeStampDisplay.place(anchor='nw', relx=SharedVars.GuiFrdOtherLeftX, rely=SharedVars.GuiFrdTimeStampTopY)

	# Sifting
	SharedVars.GuiSiftButton.place(anchor='se', relx=0.85, rely=0.99)

	# Miscellaneous
	SharedVars.GuiDevelopmentMessageLabel.place(anchor='sw', relx=0.01,rely=0.99)
	SharedVars.GuiExitButton.place(anchor='se', relx=0.99, rely=0.99)

def GuiLogDateListBoxCallback(ListboxEvent):
	lb = ListboxEvent.widget
	ListboxSelectionIndex = int(lb.curselection()[0])
	SelectedDateText = lb.get(ListboxSelectionIndex)
	SharedVars.GuiLogFilesListBox.delete(0, tkinter.END)
	SharedVars.GuiStrikePriceListBox.delete(0, tkinter.END)
	SharedVars.GuiExpirationDateListBox.delete(0, tkinter.END)
	SharedVars.GuiTimestampListBox.delete(0, tkinter.END)
	IbDataSifterStorage.SelectLogDate(SelectedDateText)

def GuiFillLoggedFilesListBox(SelectedDateText):
	SharedVars.GuiLogFilesListBoxLabel.configure(text='Files logged on ' + SharedVars.CurrentlyOpenTradedDayDirectory)
	SharedVars.GuiLogFilesListBox.delete(0, tkinter.END)
	for FileName in SharedVars.LoggedFilesInCurrentDate:
		SharedVars.GuiLogFilesListBox.insert(tkinter.END, FileName)

def GuiLoggedFilesListBoxCallback(ListboxEvent):
	lb = ListboxEvent.widget
	ListboxSelectionIndex = int(lb.curselection()[0])
	FileName = lb.get(ListboxSelectionIndex)
	SharedVars.GuiTimestampListBox.delete(0, tkinter.END)
	IbDataSifterStorage.SelectLogFile(FileName)

def GuiFillStrikePriceListBox():
	SharedVars.GuiStrikePriceListBox.delete(0, tkinter.END)
	for StrikePrice in SharedVars.LoggedStrikePricesInCurrentDate:
		SharedVars.GuiStrikePriceListBox.insert(tkinter.END, StrikePrice)

def GuiFillExpirationDateListBox():
	SharedVars.GuiExpirationDateListBox.delete(0, tkinter.END)
	for ExpirationDate in SharedVars.LoggedExpirationDatesInCurrentDate:
		SharedVars.GuiExpirationDateListBox.insert(tkinter.END, ExpirationDate)

def GuiFillTimestampListBox():
	GuiClearFileRecordDisplay()
	SharedVars.GuiTimestampListBox.delete(0, tkinter.END)
	SelectedFile = SharedVars.ImportedDataFileCache[SharedVars.SelectedFileCacheIndex]
	for ValidIndex in SelectedFile['ValidRecordIndexList']:
		ValidFileRecord = SelectedFile['FileRecordList'][ValidIndex]
		Timestamp = ValidFileRecord['Timestamp']
		SharedVars.GuiTimestampListBox.insert(tkinter.END, IbDataSifterUtilities.StringFormatTimestamp(Timestamp))

def GuiTimestampListBoxCallBack(ListboxEvent):
	lb = ListboxEvent.widget
	ListboxSelectionIndex = int(lb.curselection()[0])
	SelectedFile = SharedVars.ImportedDataFileCache[SharedVars.SelectedFileCacheIndex]
	ValidRecordIndexesInCurrentFile = SelectedFile['ValidRecordIndexList']
	AllRecordsInFile = SelectedFile['FileRecordList']
	FileRecordIndex = ValidRecordIndexesInCurrentFile[ListboxSelectionIndex]
	FileRecordToDisplay = AllRecordsInFile[FileRecordIndex]
	GuiShowFileRecord(FileRecordToDisplay)

def GuiShowUnderlyingSummary(Open, High, Low, Close):
	if High < Low:
		GuiClearUnderlyingSummary()
	else:
		SharedVars.GuiUnderlyingLabel.configure(text='SPX Open: ' + IbDataSifterUtilities.StringFormatDollars(Open) +
													', High: ' + IbDataSifterUtilities.StringFormatDollars(High) +
													', Low: ' + IbDataSifterUtilities.StringFormatDollars(Low) +
													', Close: ' + IbDataSifterUtilities.StringFormatDollars(Close))

def GuiClearUnderlyingSummary():
		SharedVars.GuiUnderlyingLabel.configure(text='Underlying: open=----.--, high=----.--, low=----.--, close=----.--')

def GuiShowFileRecord(FileRecord):
	MonitorData = FileRecord['MonitorData']
	Ask = MonitorData['Ask']
	Bid = MonitorData['Bid']
	Last = MonitorData['Last']
	Model = MonitorData['Model']
	SharedVars.GuiFrdRecordTimestampDisplay.configure(text='File timestamp: ' + IbDataSifterUtilities.StringFormatTimestamp(FileRecord['Timestamp']))
	SharedVars.GuiFrdAskPriceDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(Ask['Price']))
	SharedVars.GuiFrdAskSizeDisplay.configure(text=str(Ask['Size']))
	SharedVars.GuiFrdAskImpliedVolatilityDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Ask['ImpliedVolatility']))
	SharedVars.GuiFrdAskDeltaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Ask['Delta']))
	SharedVars.GuiFrdAskThetaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Ask['Theta']))
	SharedVars.GuiFrdAskGammaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Ask['Gamma']))
	SharedVars.GuiFrdAskVegaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Ask['Vega']))
	SharedVars.GuiFrdBidPriceDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(Bid['Price']))
	SharedVars.GuiFrdBidSizeDisplay.configure(text=str(Bid['Size']))
	SharedVars.GuiFrdBidImpliedVolatilityDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Bid['ImpliedVolatility']))
	SharedVars.GuiFrdBidDeltaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Bid['Delta']))
	SharedVars.GuiFrdBidThetaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Bid['Theta']))
	SharedVars.GuiFrdBidGammaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Bid['Gamma']))
	SharedVars.GuiFrdBidVegaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Bid['Vega']))
	SharedVars.GuiFrdLastPriceDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(Last['Price']))
	SharedVars.GuiFrdLastSizeDisplay.configure(text=str(Last['Size']))
	SharedVars.GuiFrdLastImpliedVolatilityDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Last['ImpliedVolatility']))
	SharedVars.GuiFrdLastDeltaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Last['Delta']))
	SharedVars.GuiFrdLastThetaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Last['Theta']))
	SharedVars.GuiFrdLastGammaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Last['Gamma']))
	SharedVars.GuiFrdLastVegaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Last['Vega']))
	SharedVars.GuiFrdModelPriceDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(Model['Price']))
	SharedVars.GuiFrdModelSizeDisplay.configure(text=str(Model['Size']))
	SharedVars.GuiFrdModelImpliedVolatilityDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Model['ImpliedVolatility']))
	SharedVars.GuiFrdModelDeltaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Model['Delta']))
	SharedVars.GuiFrdModelThetaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Model['Theta']))
	SharedVars.GuiFrdModelGammaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Model['Gamma']))
	SharedVars.GuiFrdModelVegaDisplay.configure(text=IbDataSifterUtilities.StringFormatGreek(Model['Vega']))
	SharedVars.GuiFrdOpenDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(MonitorData['Open']))
	SharedVars.GuiFrdHighDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(MonitorData['High']))
	SharedVars.GuiFrdLowDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(MonitorData['Low']))
	SharedVars.GuiFrdCloseDisplay.configure(text=IbDataSifterUtilities.StringFormatDollars(MonitorData['Close']))
	SharedVars.GuiFrdVolumeDisplay.configure(text=str(MonitorData['Volume']))
	# SharedVars.GuiFrdTimeStampDisplay.configure(text=IbDataSifterUtilities.StringFormatTimestamp(MonitorData['TimeStamp']))
	SharedVars.GuiFrdTimeStampDisplay.configure(text=(MonitorData['TimeStamp']))

def GuiClearFileRecordDisplay():
	SharedVars.GuiFrdRecordTimestampDisplay.configure(text='')
	SharedVars.GuiFrdAskPriceDisplay.configure(text='')
	SharedVars.GuiFrdAskSizeDisplay.configure(text='')
	SharedVars.GuiFrdAskImpliedVolatilityDisplay.configure(text='')
	SharedVars.GuiFrdAskDeltaDisplay.configure(text='')
	SharedVars.GuiFrdAskThetaDisplay.configure(text='')
	SharedVars.GuiFrdAskGammaDisplay.configure(text='')
	SharedVars.GuiFrdAskVegaDisplay.configure(text='')
	SharedVars.GuiFrdBidPriceDisplay.configure(text='')
	SharedVars.GuiFrdBidSizeDisplay.configure(text='')
	SharedVars.GuiFrdBidImpliedVolatilityDisplay.configure(text='')
	SharedVars.GuiFrdBidDeltaDisplay.configure(text='')
	SharedVars.GuiFrdBidThetaDisplay.configure(text='')
	SharedVars.GuiFrdBidGammaDisplay.configure(text='')
	SharedVars.GuiFrdBidVegaDisplay.configure(text='')
	SharedVars.GuiFrdLastPriceDisplay.configure(text='')
	SharedVars.GuiFrdLastSizeDisplay.configure(text='')
	SharedVars.GuiFrdLastImpliedVolatilityDisplay.configure(text='')
	SharedVars.GuiFrdLastDeltaDisplay.configure(text='')
	SharedVars.GuiFrdLastThetaDisplay.configure(text='')
	SharedVars.GuiFrdLastGammaDisplay.configure(text='')
	SharedVars.GuiFrdLastVegaDisplay.configure(text='')
	SharedVars.GuiFrdModelPriceDisplay.configure(text='')
	SharedVars.GuiFrdModelSizeDisplay.configure(text='')
	SharedVars.GuiFrdModelImpliedVolatilityDisplay.configure(text='')
	SharedVars.GuiFrdModelDeltaDisplay.configure(text='')
	SharedVars.GuiFrdModelThetaDisplay.configure(text='')
	SharedVars.GuiFrdModelGammaDisplay.configure(text='')
	SharedVars.GuiFrdModelVegaDisplay.configure(text='')
	SharedVars.GuiFrdOpenDisplay.configure(text='')
	SharedVars.GuiFrdHighDisplay.configure(text='')
	SharedVars.GuiFrdLowDisplay.configure(text='')
	SharedVars.GuiFrdCloseDisplay.configure(text='')
	SharedVars.GuiFrdVolumeDisplay.configure(text='')
	SharedVars.GuiFrdTimeStampDisplay.configure(text='')

def InitializeProgressBar(LabelText):
	SharedVars.GuiProgressBarLabel.configure(text = LabelText)
	SharedVars.GuiProgressBar['value'] = 0.0

def UpdateProgressBar(PercentageComplete):
	SharedVars.GuiProgressBar['value'] = PercentageComplete

def CloseProgressBar():
	SharedVars.GuiProgressBarLabel.configure(text='')
	SharedVars.GuiProgressBar['value'] = 0.0

def GuiSiftButton_Clicked():
	IbDataSifter.Sift()

def GuiShowDevelopmentMessage(Text):
	SharedVars.GuiDevelopmentMessageLabel.configure(text=Text)

def RefreshGui():
	SharedVars.GuiInputPathLabel.configure(text='Input directory: ' + SharedVars.InputDirectoryPath)
	SharedVars.GuiOutputPathLabel.configure(text='Output directory: ' + SharedVars.OutputDirectoryPath)
	SharedVars.GuiWindow.after(SharedVars.GuiRefreshInterval, RefreshGui)

def ExitGui():
	SharedVars.BackgroundRunning = False
	SharedVars.GuiWindow.destroy()

