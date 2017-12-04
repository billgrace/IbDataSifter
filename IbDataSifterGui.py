import time
import tkinter

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

	# File system - paths
	SharedVars.GuiInputPathLabel.place(anchor='nw', relx=0.01,rely=0.04)
	SharedVars.GuiOutputPathLabel.place(anchor='nw', relx=0.01,rely=0.08)
	# File system - logged data date list
	SharedVars.GuiLogDateListBoxLabel.place(anchor='nw', relx=SharedVars.GuiLogDateListBoxLeftX,rely=SharedVars.GuiListBoxLabelTopY)
	SharedVars.GuiLogDateListBox.place(anchor='nw', relx=SharedVars.GuiLogDateListBoxLeftX,rely=SharedVars.GuiListBoxTopY)
	SharedVars.GuiLogDateListBox.configure(width=10, height=SharedVars.GuiListBoxHeight)
	SharedVars.GuiLogDateListBox.bind('<<ListboxSelect>>', GuiLogDateListBoxCallback)
	for date in SharedVars.TradedDayDirectories:
		SharedVars.GuiLogDateListBox.insert(tkinter.END, date)
	# File system - logged data file list
	SharedVars.GuiLogFilesListBoxLabel.place(anchor='nw', relx=SharedVars.GuiLogFilesListBoxLeftX,rely=SharedVars.GuiListBoxLabelTopY)
	SharedVars.GuiLogFilesListBox.place(anchor='nw', relx=0.21, rely=SharedVars.GuiListBoxTopY)
	SharedVars.GuiLogFilesListBox.configure(width=22,height=SharedVars.GuiListBoxHeight)
	SharedVars.GuiLogFilesListBox.bind('<<ListboxSelect>>', GuiLoggedFilesListBoxCallback)
	# File system - Logged day summary
	SharedVars.GuiUnderlyingLabel.place(anchor='nw', relx=SharedVars.GuiUnderlyingSummaryLeftX,rely=SharedVars.GuiListBoxLabelTopY)
	SharedVars.GuiStrikePriceListBoxLabel.place(anchor='nw', relx=SharedVars.GuiUnderlyingSummaryLeftX,rely=SharedVars.GuiListBoxLabelTopY+0.05)
	SharedVars.GuiStrikePriceListBox.place(anchor='nw', relx=SharedVars.GuiUnderlyingSummaryLeftX,rely=SharedVars.GuiListBoxLabelTopY+0.10)
	SharedVars.GuiExpirationDateListBoxLabel.place(anchor='nw', relx=SharedVars.GuiUnderlyingSummaryLeftX+0.25,rely=SharedVars.GuiListBoxLabelTopY+0.05)
	SharedVars.GuiExpirationDateListBox.place(anchor='nw', relx=SharedVars.GuiUnderlyingSummaryLeftX+0.25,rely=SharedVars.GuiListBoxLabelTopY+0.10)

	# Sifting
	SharedVars.GuiSiftButton.place(anchor='se', relx=0.85, rely=0.99)

	# Miscellaneous
	SharedVars.GuiDevelopmentMessageLabel.place(anchor='sw', relx=0.01,rely=0.99)
	SharedVars.GuiExitButton.place(anchor='se', relx=0.99, rely=0.99)

def GuiSiftButton_Clicked():
	IbDataSifter.Sift()

def GuiLogDateListBoxCallback(ListboxEvent):
	lb = ListboxEvent.widget
	ListboxSelectionIndex = int(lb.curselection()[0])
	SelectedDateText = lb.get(ListboxSelectionIndex)
	IbDataSifterStorage.SelectLogDate(SelectedDateText)

def GuiLoggedFilesListBoxCallback(ListboxEvent):
	lb = ListboxEvent.widget
	ListboxSelectionIndex = int(lb.curselection()[0])
	FileName = lb.get(ListboxSelectionIndex)
	IbDataSifterStorage.SelectLogFile(FileName)

def GuiFillLoggedFilesListBox(SelectedDateText):
	SharedVars.GuiLogFilesListBoxLabel.configure(text='Files logged on ' + SharedVars.CurrentlyOpenTradedDayDirectory)
	SharedVars.GuiLogFilesListBox.delete(0, tkinter.END)
	for FileName in SharedVars.LoggedFilesInCurrentDate:
		SharedVars.GuiLogFilesListBox.insert(tkinter.END, FileName)

def GuiFillStrikePriceListBox():
	SharedVars.GuiStrikePriceListBox.delete(0, tkinter.END)
	for StrikePrice in SharedVars.LoggedStrikePricesInCurrentDate:
		SharedVars.GuiStrikePriceListBox.insert(tkinter.END, StrikePrice)

def GuiFillExpirationDateListBox():
	SharedVars.GuiExpirationDateListBox.delete(0, tkinter.END)
	for ExpirationDate in SharedVars.LoggedExpirationDatesInCurrentDate:
		SharedVars.GuiExpirationDateListBox.insert(tkinter.END, ExpirationDate)

def RefreshGui():
	SharedVars.GuiInputPathLabel.configure(text='Input directory: ' + SharedVars.InputDirectoryPath)
	SharedVars.GuiOutputPathLabel.configure(text='Output directory: ' + SharedVars.OutputDirectoryPath)
	SharedVars.GuiWindow.after(SharedVars.GuiRefreshInterval, RefreshGui)

def ExitGui():
	# global BackgroundRunning
	SharedVars.BackgroundRunning = False
	SharedVars.GuiWindow.destroy()

