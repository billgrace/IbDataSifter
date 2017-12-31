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
	SharedVars.GuiStrikePriceListBox.configure(width=SharedVars.GuiStrikePriceListBoxWidth, height=SharedVars.GuiStrikePriceListBoxHeight)

	# Expiration date list
	SharedVars.GuiExpirationDateListBoxLabel.place(anchor='nw', relx=SharedVars.GuiExpirationDateListBoxLabelLeftX,rely=SharedVars.GuiExpirationDateListBoxLabelTopY)
	SharedVars.GuiExpirationDateListBox.place(anchor='nw', relx=SharedVars.GuiExpirationDateListBoxLeftX,rely=SharedVars.GuiExpirationDateListBoxTopY)
	SharedVars.GuiExpirationDateListBox.configure(width=SharedVars.GuiExpirationDateListBoxWidth, height=SharedVars.GuiExpirationDateListBoxHeight)

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
	SharedVars.GuiTimestampListBox.delete(0, tkinter.END)
	for Timestamp in SharedVars.TimestampsInCurrentFile:
		SharedVars.GuiTimestampListBox.insert(tkinter.END, IbDataSifterUtilities.StringFormatTimestamp(Timestamp))

def GuiTimestampListBoxCallBack(ListboxEvent):
	lb = ListboxEvent.widget
	ListboxSelectionIndex = int(lb.curselection()[0])
	FileRecordIndex = SharedVars.ValidRecordIndexesInCurrentFile[ListboxSelectionIndex]
	FileRecordToDisplay = SharedVars.ValidRecordIndexesInCurrentFile[FileRecordIndex]

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

