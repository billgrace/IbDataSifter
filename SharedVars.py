import tkinter
import IbDataSifterGui

# Preferences file items
InputDirectoryPath = ''
OutputDirectoryPath = ''

# Storage items
TradedDayDirectories = []

# Gui
GuiRefreshInterval = 300
GuiWindow = tkinter.Tk()

# Gui - File system
GuiInputPathLabel = tkinter.Label(GuiWindow)
GuiOutputPathLabel = tkinter.Label(GuiWindow)
GuiLogDateListBox = tkinter.Listbox(GuiWindow)

# Gui - Sifting
GuiSiftButton = tkinter.Button(GuiWindow, text='Sift', command=IbDataSifterGui.GuiSiftButton_Clicked)

# Gui - Miscellaneous
GuiMessageLabel = tkinter.Label(GuiWindow, text='Initial GuiMessageLabel text', fg='#055', bg='#8ff')
GuiExitButton = tkinter.Button(GuiWindow, text='Exit', command=IbDataSifterGui.ExitGui)
