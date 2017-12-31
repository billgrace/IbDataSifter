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
TimestampsInCurrentFile = []
ValidRecordIndexesInCurrentFile = []

# Imported data
LogDateDirectoryPath = ''
ImportedDataFileCache = []
UnderlyingOpen = 0.0
UnderlyingHigh = 0.0
UnderlyingLow = 0.0
UnderlyingClose = 0.0

# Gui - General
GuiMainWindowWidth = 1000
GuiMainWindowHeight = 700
GuiMainWindowLeft = 10
GuiMainWindowTop = 10
GuiRefreshInterval = 300
GuiWindow = tk.Tk()

# Gui - File path display
GuiInputPathLabelLeftX = 0.01
GuiInputPathLabelTopY = 0.04
GuiOutputPathLabelLeftX = 0.01
GuiOutputPathLabelTopY = 0.08
GuiInputPathLabel = tk.Label(GuiWindow)
GuiOutputPathLabel = tk.Label(GuiWindow)

# Gui - Logged date list box
GuiLogDateListBoxLabelLeftX = 0.01
GuiLogDateListBoxLabelTopY = 0.14
GuiLogDateListBoxLeftX = GuiLogDateListBoxLabelLeftX
GuiLogDateListBoxTopY = GuiLogDateListBoxLabelTopY + 0.04
GuiLogDateListBoxWidth = 10
GuiLogDateListBoxHeight = 14
GuiLogDateListBoxLabel = tk.Label(GuiWindow, text='Logged dates')
GuiLogDateListBox = tk.Listbox(GuiWindow)

# Gui - Logged file list box
GuiLogFilesListBoxLabelLeftX = 0.12
GuiLogFilesListBoxLabelTopY = GuiLogDateListBoxLabelTopY
GuiLogFilesListBoxLeftX = GuiLogFilesListBoxLabelLeftX
GuiLogFilesListBoxTopY = GuiLogFilesListBoxLabelTopY + 0.04
GuiLogFilesListBoxWidth = 22
GuiLogFilesListBoxHeight = GuiLogDateListBoxHeight
GuiLogFilesListBoxLabel = tk.Label(GuiWindow, text='Files logged on - - -')
GuiLogFilesListBox = tk.Listbox(GuiWindow)

# Gui - Strike price list box
GuiStrikePriceListBoxLabelLeftX = 0.01
GuiStrikePriceListBoxLabelTopY = 0.54
GuiStrikePriceListBoxLeftX = GuiStrikePriceListBoxLabelLeftX
GuiStrikePriceListBoxTopY = GuiStrikePriceListBoxLabelTopY + 0.04
GuiStrikePriceListBoxWidth = 10
GuiStrikePriceListBoxHeight = 11
GuiStrikePriceListBoxLabel = tk.Label(GuiWindow, text='Strike prices')
GuiStrikePriceListBox = tk.Listbox(GuiWindow)

# Gui - Expiration date list box
GuiExpirationDateListBoxLabelLeftX = 0.12
GuiExpirationDateListBoxLabelTopY = GuiStrikePriceListBoxLabelTopY
GuiExpirationDateListBoxLeftX = GuiExpirationDateListBoxLabelLeftX
GuiExpirationDateListBoxTopY = GuiExpirationDateListBoxLabelTopY + 0.04
GuiExpirationDateListBoxWidth = 10
GuiExpirationDateListBoxHeight = GuiStrikePriceListBoxHeight
GuiExpirationDateListBoxLabel = tk.Label(GuiWindow, text='Expiration dates')
GuiExpirationDateListBox = tk.Listbox(GuiWindow)

# Gui - Progress bar
GuiProgressBarLabelLeftX = 0.01
GuiProgressBarLabelTopY = 0.92
GuiProgressBarLeftX = 0.21
GuiProgressBarTopY = GuiProgressBarLabelTopY
GuiProgressBarLabel = tk.Label(GuiWindow)
GuiProgressBar = tk.ttk.Progressbar(GuiWindow, orient='horizontal')

# Gui - Underlying summary
GuiUnderlyingSummaryLeftX = 0.01
GuiUnderlyingSummaryTopY = 0.88
GuiUnderlyingLabel = tk.Label(GuiWindow)

# Gui - Timestamps
GuiTimestampListBoxLabelLeftX = 0.34
GuiTimestampListBoxLabelTopY = GuiLogDateListBoxLabelTopY
GuiTimestampListBoxLeftX = GuiTimestampListBoxLabelLeftX
GuiTimestampListBoxTopY = GuiTimestampListBoxLabelTopY + 0.04
GuiTimestampListBoxWidth = 10
GuiTimestampListBoxHeight = 25
GuiTimestampListBoxLabel = tk.Label(GuiWindow, text='Timestamps')
GuiTimestampListBox = tk.Listbox(GuiWindow)

# Gui - Sifting
GuiSiftButton = tk.Button(GuiWindow, text='Sift', command=IbDataSifterGui.GuiSiftButton_Clicked)

# Gui - Miscellaneous
GuiDevelopmentMessageLabel = tk.Label(GuiWindow, text='(---)', fg='#055', bg='#8ff')
GuiExitButton = tk.Button(GuiWindow, text='Exit', command=IbDataSifterGui.ExitGui)

# Schemas
MonitorDataReaderSchema = avro.schema.Parse(open("schemas/MonitorDataReaderSchema.txt").read())
