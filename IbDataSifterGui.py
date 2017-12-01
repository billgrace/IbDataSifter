import time
import tkinter

import IbDataSifter
import IbDataSifterStorage
import SharedVars

def PrepareGui():
	GuiMainWindowLeft = 10
	GuiMainWindowTop = 10
	GuiMainWindowWidth = 800
	GuiMainWindowHeight = 600
	GuiMainWindowBackgroundColor = 'magenta'
	SharedVars.GuiWindow.geometry(str(GuiMainWindowWidth) + 'x' + str(GuiMainWindowHeight) + '+' + str(GuiMainWindowLeft) + '+' + str(GuiMainWindowTop))
	SharedVars.GuiWindow.configure(background=GuiMainWindowBackgroundColor)
	SharedVars.GuiWindow.resizable(True, True)

	# File system - paths
	SharedVars.GuiInputPathLabel.place(anchor='nw', relx=0.01,rely=0.04)
	SharedVars.GuiOutputPathLabel.place(anchor='nw', relx=0.01,rely=0.08)
	# File system - logged data date list
	GuiListBoxLabelTopY = 0.14
	GuiListBoxTopY = 0.18
	GuiListBoxHeight = 10
	GuiLogDateListBoxLeftX = 0.01
	SharedVars.GuiLogDateListBoxLabel.place(anchor='nw', relx=GuiLogDateListBoxLeftX,rely=GuiListBoxLabelTopY)
	SharedVars.GuiLogDateListBox.place(anchor='nw', relx=GuiLogDateListBoxLeftX,rely=GuiListBoxTopY)
	SharedVars.GuiLogDateListBox.configure(width=10, height=GuiListBoxHeight)
	SharedVars.GuiLogDateListBox.bind('<<ListboxSelect>>', GuiLogDateListBoxCallback)
	for date in SharedVars.TradedDayDirectories:
		SharedVars.GuiLogDateListBox.insert(tkinter.END, date)
	# File system - logged data file list
	GuiLogFilesListBoxLeftX = 0.21
	SharedVars.GuiLogFilesListBoxLabel.place(anchor='nw', relx=GuiLogFilesListBoxLeftX,rely=GuiListBoxLabelTopY)
	SharedVars.GuiLogFilesListBox.place(anchor='nw', relx=0.21, rely=GuiListBoxTopY)
	SharedVars.GuiLogFilesListBox.configure(width=22,height=GuiListBoxHeight)
	SharedVars.GuiLogFilesListBox.bind('<<ListboxSelect>>', GuiLoggedFilesListBoxCallback)
	# File system - Logged day summary
	GuiUnderlyingSummaryLeftX = 0.51
	SharedVars.GuiUnderlyingLabel.place(anchor='nw', relx=GuiUnderlyingSummaryLeftX,rely=GuiListBoxLabelTopY)
	SharedVars.GuiStrikePriceListBoxLabel.place(anchor='nw', relx=GuiUnderlyingSummaryLeftX,rely=GuiListBoxLabelTopY+0.05)
	SharedVars.GuiStrikePriceListBox.place(anchor='nw', relx=GuiUnderlyingSummaryLeftX,rely=GuiListBoxLabelTopY+0.10)
	SharedVars.GuiExpirationDateListBoxLabel.place(anchor='nw', relx=GuiUnderlyingSummaryLeftX+0.25,rely=GuiListBoxLabelTopY+0.05)
	SharedVars.GuiExpirationDateListBox.place(anchor='nw', relx=GuiUnderlyingSummaryLeftX+0.25,rely=GuiListBoxLabelTopY+0.10)

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

