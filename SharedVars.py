import tkinter
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
GuiWindow = tkinter.Tk()

# Gui - Directory paths
GuiInputPathLabel = tkinter.Label(GuiWindow)
GuiOutputPathLabel = tkinter.Label(GuiWindow)

# Gui - Logged data selection and display
GuiLogDateListBoxLabel = tkinter.Label(GuiWindow, text='Logged data dates')
GuiLogDateListBox = tkinter.Listbox(GuiWindow)
GuiLogFilesListBoxLabel = tkinter.Label(GuiWindow, text='Files logged on - - -')
GuiUnderlyingLabel = tkinter.Label(GuiWindow, text='Underlying: open=1234.56, high=1234.56, low=1234.56, close=1234.56')
GuiLogFilesListBox = tkinter.Listbox(GuiWindow)
GuiStrikePriceListBoxLabel = tkinter.Label(GuiWindow, text='Strike prices')
GuiStrikePriceListBox = tkinter.Listbox(GuiWindow)
GuiExpirationDateListBoxLabel = tkinter.Label(GuiWindow, text='Expiration dates')
GuiExpirationDateListBox = tkinter.Listbox(GuiWindow)

# Gui - Sifting
GuiSiftButton = tkinter.Button(GuiWindow, text='Sift', command=IbDataSifterGui.GuiSiftButton_Clicked)

# Gui - Miscellaneous
GuiDevelopmentMessageLabel = tkinter.Label(GuiWindow, text='(development message space)', fg='#055', bg='#8ff')
GuiExitButton = tkinter.Button(GuiWindow, text='Exit', command=IbDataSifterGui.ExitGui)

# Schemas
MonitorDataReaderSchema = avro.schema.Parse(open("schemas/MonitorDataReaderSchema.txt").read())
