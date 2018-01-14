import tkinter as tk
from tkinter import ttk
import avro.schema
import IbDataSifterClasses
import IbDataSifterGui

# Preferences file items
InputDirectoryPath = ''
OutputDirectoryPath = ''

# Storage items
LogDateDirectoryPath = ''
TradedDayDirectories = []
ImportedDataFileCache = []
CurrentlyOpenTradedDayDirectory = 'YYYY-MM-DD'
LoggedFilesInCurrentDate = []
LoggedStrikePricesInCurrentDate = []
LoggedExpirationDatesInCurrentDate = []
SelectedFileCacheIndex = 0

# Underlying summary
UnderlyingOpen = 0.0
UnderlyingHigh = 0.0
UnderlyingLow = 0.0
UnderlyingClose = 0.0

# Gui - General
GuiMainWindowWidth = 1100
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
GuiProgressBarLeftX = 0.31
GuiProgressBarTopY = GuiProgressBarLabelTopY
GuiProgressBarLabel = tk.Label(GuiWindow)
GuiProgressBar = tk.ttk.Progressbar(GuiWindow, orient='horizontal')

# Gui - Underlying summary
GuiUnderlyingSummaryLeftX = 0.01
GuiUnderlyingSummaryTopY = 0.88
GuiUnderlyingLabel = tk.Label(GuiWindow)

# Gui - Timestamps
GuiTimestampListBoxLabelLeftX = 0.33
GuiTimestampListBoxLabelTopY = GuiLogDateListBoxLabelTopY
GuiTimestampListBoxLeftX = GuiTimestampListBoxLabelLeftX
GuiTimestampListBoxTopY = GuiTimestampListBoxLabelTopY + 0.04
GuiTimestampListBoxWidth = 10
GuiTimestampListBoxHeight = 25
GuiTimestampListBoxLabel = tk.Label(GuiWindow, text='Timestamps')
GuiTimestampListBox = tk.Listbox(GuiWindow)

# Gui - File record display - labels
GuiFrdFilenameDisplayLeftX = 0.52
GuiFrdFilenameDisplayTopY = 0.16
GuiFrdRecordTimestampLeftX = GuiFrdFilenameDisplayLeftX
GuiFrdRecordTimestampTopY = GuiFrdFilenameDisplayTopY + 0.04
GuiFrdPriceLeftX = GuiFrdRecordTimestampLeftX
GuiFrdSizeLeftX = GuiFrdPriceLeftX + 0.07
GuiFrdImpliedVolatilityLeftX = GuiFrdPriceLeftX + 0.14
GuiFrdDeltaLeftX = GuiFrdPriceLeftX + 0.21
GuiFrdThetaLeftX = GuiFrdPriceLeftX + 0.28
GuiFrdGammaLeftX = GuiFrdPriceLeftX + 0.35
GuiFrdVegaLeftX = GuiFrdPriceLeftX + 0.42
GuiFrdGreekLabelTopY = GuiFrdRecordTimestampTopY + 0.05
GuiFrdABLMLabelRightX = GuiFrdPriceLeftX - 0.01
GuiFrdAskTopY = GuiFrdRecordTimestampTopY + 0.09
GuiFrdBidTopY = GuiFrdRecordTimestampTopY + 0.13
GuiFrdLastTopY = GuiFrdRecordTimestampTopY + 0.17
GuiFrdModelTopY = GuiFrdRecordTimestampTopY + 0.21
GuiFrdOtherLeftX = GuiFrdRecordTimestampLeftX
GuiFrdOtherLabelRightX = GuiFrdOtherLeftX - 0.01
GuiFrdOpenTopY = GuiFrdRecordTimestampTopY + 0.26
GuiFrdHighTopY = GuiFrdOpenTopY + 0.04
GuiFrdLowTopY = GuiFrdOpenTopY + 0.08
GuiFrdCloseTopY = GuiFrdOpenTopY + 0.12
GuiFrdVolumeTopY = GuiFrdOpenTopY + 0.16
GuiFrdTimeStampTopY = GuiFrdOpenTopY + 0.20
GuiFrdRecordTimestampDisplay = tk.Label(GuiWindow)
GuiFrdPriceLabel = tk.Label(GuiWindow)
GuiFrdSizeLabel = tk.Label(GuiWindow)
GuiFrdImpliedVolatilityLabel = tk.Label(GuiWindow)
GuiFrdDeltaLabel = tk.Label(GuiWindow)
GuiFrdThetaLabel = tk.Label(GuiWindow)
GuiFrdGammaLabel = tk.Label(GuiWindow)
GuiFrdVegaLabel = tk.Label(GuiWindow)
GuiFrdAskLabel = tk.Label(GuiWindow)
GuiFrdBidLabel = tk.Label(GuiWindow)
GuiFrdLastLabel = tk.Label(GuiWindow)
GuiFrdModelLabel = tk.Label(GuiWindow)
GuiFrdOpenLabel = tk.Label(GuiWindow)
GuiFrdHighLabel = tk.Label(GuiWindow)
GuiFrdLowLabel = tk.Label(GuiWindow)
GuiFrdCloseLabel = tk.Label(GuiWindow)
GuiFrdVolumeLabel = tk.Label(GuiWindow)
GuiFrdTimeStampLabel = tk.Label(GuiWindow)

# Gui - File record display - fields
GuiFrdFilenameDisplay = tk.Label(GuiWindow)
GuiFrdAskPriceDisplay = tk.Label(GuiWindow)
GuiFrdAskSizeDisplay = tk.Label(GuiWindow)
GuiFrdAskImpliedVolatilityDisplay = tk.Label(GuiWindow)
GuiFrdAskDeltaDisplay = tk.Label(GuiWindow)
GuiFrdAskThetaDisplay = tk.Label(GuiWindow)
GuiFrdAskGammaDisplay = tk.Label(GuiWindow)
GuiFrdAskVegaDisplay = tk.Label(GuiWindow)
GuiFrdBidPriceDisplay = tk.Label(GuiWindow)
GuiFrdBidSizeDisplay = tk.Label(GuiWindow)
GuiFrdBidImpliedVolatilityDisplay = tk.Label(GuiWindow)
GuiFrdBidDeltaDisplay = tk.Label(GuiWindow)
GuiFrdBidThetaDisplay = tk.Label(GuiWindow)
GuiFrdBidGammaDisplay = tk.Label(GuiWindow)
GuiFrdBidVegaDisplay = tk.Label(GuiWindow)
GuiFrdLastPriceDisplay = tk.Label(GuiWindow)
GuiFrdLastSizeDisplay = tk.Label(GuiWindow)
GuiFrdLastImpliedVolatilityDisplay = tk.Label(GuiWindow)
GuiFrdLastDeltaDisplay = tk.Label(GuiWindow)
GuiFrdLastThetaDisplay = tk.Label(GuiWindow)
GuiFrdLastGammaDisplay = tk.Label(GuiWindow)
GuiFrdLastVegaDisplay = tk.Label(GuiWindow)
GuiFrdModelPriceDisplay = tk.Label(GuiWindow)
GuiFrdModelSizeDisplay = tk.Label(GuiWindow)
GuiFrdModelImpliedVolatilityDisplay = tk.Label(GuiWindow)
GuiFrdModelDeltaDisplay = tk.Label(GuiWindow)
GuiFrdModelThetaDisplay = tk.Label(GuiWindow)
GuiFrdModelGammaDisplay = tk.Label(GuiWindow)
GuiFrdModelVegaDisplay = tk.Label(GuiWindow)
GuiFrdOpenDisplay = tk.Label(GuiWindow)
GuiFrdHighDisplay = tk.Label(GuiWindow)
GuiFrdLowDisplay = tk.Label(GuiWindow)
GuiFrdCloseDisplay = tk.Label(GuiWindow)
GuiFrdVolumeDisplay = tk.Label(GuiWindow)
GuiFrdTimeStampDisplay = tk.Label(GuiWindow)

# Gui - Sifting
GuiSiftButton = tk.Button(GuiWindow, text='Sift', command=IbDataSifterGui.GuiSiftButton_Clicked)

# Gui - Miscellaneous
GuiDevelopmentMessageLabel = tk.Label(GuiWindow, text='(---)', fg='#055', bg='#8ff')
GuiExitButton = tk.Button(GuiWindow, text='Exit', command=IbDataSifterGui.ExitGui)

# Schemas
MonitorDataReaderSchema = avro.schema.Parse(open("schemas/MonitorDataReaderSchema.txt").read())
