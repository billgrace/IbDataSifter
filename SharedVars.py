import tkinter as tk
from tkinter import ttk
import avro.schema
import IbDataSifterClasses
import IbDataSifterGui

# Preferences file items
InputDirectoryPath = ''
OutputDirectoryPath = ''

# Storage items
TradedDayDirectories = []
CurrentlyOpenTradedDayDirectory = 'YYYY-MM-DD'
LoggedFilesInCurrentDate = []
LoggedStrikePricesInCurrentDate = []
LoggedExpirationDatesInCurrentDate = []

# Imported data
LogDateDirectoryPath = ''
ImportedDataFileList = []
UnderlyingOpen = 0.0
UnderlyingHigh = 0.0
UnderlyingLow = 0.0
UnderlyingClose = 0.0

# Gui - General
GuiMainWindowWidth = 1000
GuiMainWindowHeight = 700
GuiMainWindowLeft = 10
GuiMainWindowTop = 10
GuiListBoxLabelTopY = 0.14
GuiListBoxTopY = 0.18
GuiListBoxHeight = 10
GuiLogDateListBoxLeftX = 0.01
GuiLogFilesListBoxLeftX = 0.21
GuiUnderlyingSummaryLeftX = 0.51
GuiRefreshInterval = 300
GuiWindow = tk.Tk()

# Gui - Directory paths
GuiInputPathLabel = tk.Label(GuiWindow)
GuiOutputPathLabel = tk.Label(GuiWindow)

# Gui - Logged data selection and display
GuiLogDateListBoxLabel = tk.Label(GuiWindow, text='Logged data dates')
GuiLogDateListBox = tk.Listbox(GuiWindow)
GuiLogFilesListBoxLabel = tk.Label(GuiWindow, text='Files logged on - - -')
GuiUnderlyingLabel = tk.Label(GuiWindow, text='Underlying: open=1234.56, high=1234.56, low=1234.56, close=1234.56')
GuiLogFilesListBox = tk.Listbox(GuiWindow)
GuiStrikePriceListBoxLabel = tk.Label(GuiWindow, text='Strike prices')
GuiStrikePriceListBox = tk.Listbox(GuiWindow)
GuiExpirationDateListBoxLabel = tk.Label(GuiWindow, text='Expiration dates')
GuiExpirationDateListBox = tk.Listbox(GuiWindow)

# Gui - Sifting
GuiSiftButton = tk.Button(GuiWindow, text='Sift', command=IbDataSifterGui.GuiSiftButton_Clicked)

# Gui - Miscellaneous
GuiProgressBarLabel = tk.Label(GuiWindow)
GuiProgressBar = tk.ttk.Progressbar(GuiWindow, orient='horizontal')
GuiDevelopmentMessageLabel = tk.Label(GuiWindow, text='(development message space)', fg='#055', bg='#8ff')
GuiExitButton = tk.Button(GuiWindow, text='Exit', command=IbDataSifterGui.ExitGui)

# Schemas
MonitorDataReaderSchema = avro.schema.Parse(open("schemas/MonitorDataReaderSchema.txt").read())
