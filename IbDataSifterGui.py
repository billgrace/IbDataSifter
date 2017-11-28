import time
import tkinter

import IbDataSifter
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
	# File system - logged data
	SharedVars.GuiLogDateListBox.place(anchor='nw', relx=0.01,rely=0.12)
	SharedVars.GuiLogDateListBox.configure()
	for date in SharedVars.TradedDayDirectories:
		SharedVars.GuiLogDateListBox.insert(tkinter.END, date)

	# Sifting
	SharedVars.GuiSiftButton.place(anchor='nw', relx=0.85, rely=0.20)

	# Miscellaneous
	SharedVars.GuiMessageLabel.place(anchor='sw', relx=0.01,rely=0.99)
	SharedVars.GuiExitButton.place(anchor='se', relx=0.99, rely=0.99)

def GuiSiftButton_Clicked():
	IbDataSifter.Sift()

def RefreshGui():
	SharedVars.GuiInputPathLabel.configure(text='Input directory: ' + SharedVars.InputDirectoryPath)
	SharedVars.GuiOutputPathLabel.configure(text='Output directory: ' + SharedVars.OutputDirectoryPath)
	SharedVars.GuiWindow.after(SharedVars.GuiRefreshInterval, RefreshGui)

def ExitGui():
	# global BackgroundRunning
	SharedVars.BackgroundRunning = False
	SharedVars.GuiWindow.destroy()

