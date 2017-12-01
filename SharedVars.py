import tkinter
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

# Gui
GuiRefreshInterval = 300
GuiWindow = tkinter.Tk()

# Gui - File system
GuiInputPathLabel = tkinter.Label(GuiWindow)
GuiOutputPathLabel = tkinter.Label(GuiWindow)
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
