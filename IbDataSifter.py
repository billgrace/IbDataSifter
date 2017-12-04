#!/usr/local/bin/python3
import sys

import SharedVars
import IbDataSifterClasses
import IbDataSifterGui
import IbDataSifterUtilities
import IbDataSifterStorage

def Main():
	IbDataSifterUtilities.InitializeEventBindings()
	IbDataSifterStorage.ReadPreferencesFile()
	IbDataSifterStorage.PrepareDataStorage()
	IbDataSifterGui.PrepareGui()
	IbDataSifterGui.RefreshGui()
	SharedVars.GuiWindow.mainloop()

def Sift():
	for TradedDay in SharedVars.TradedDayDirectories:
		SiftTradedDay(TradedDay)
		
def SiftTradedDay(TradedDay):
	print(TradedDay)

if __name__ == '__main__':
	Main()
