import wx
import wx.lib.buttons as buttons
import wx.lib.stattext as stattext

class DayTen(wx.Frame):

    def __init__(self,parent,title):
        super(DayTen,self).__init__(parent,title=title)

        self.initializeGrid()
        self.InitUI()
        self.Centre()

    def InitUI(self):

        green = '#2eb82e'
        black = '#000000'

        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour(black)

        panelLeft = wx.Panel(mainPanel)
        panelLeft.SetFont(wx.Font(12,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        panelRight = wx.Panel(mainPanel)
        panelRight.SetBackgroundColour(green)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(panelLeft, 2, wx.EXPAND | wx.ALIGN_LEFT)
        hbox.Add(panelRight, 5, wx.EXPAND)
        mainPanel.SetSizer(hbox)

        #ADD BUTTONS
        vbox = wx.BoxSizer(wx.VERTICAL)

        autoPlayButton = buttons.GenButton(panelLeft,-1,'Auto Play')
        autoPlayButton.SetOwnBackgroundColour(black)
        autoPlayButton.SetOwnForegroundColour(green)
        autoPlayButton.SetUseFocusIndicator(False)

        stepButton = buttons.GenButton(panelLeft,-1,'Step')
        stepButton.SetOwnBackgroundColour(black)
        stepButton.SetOwnForegroundColour(green)
        stepButton.SetUseFocusIndicator(False)

        resetButton = buttons.GenButton(panelLeft,-1,'Reset')
        resetButton.SetOwnBackgroundColour(black)
        resetButton.SetOwnForegroundColour(green)
        resetButton.SetUseFocusIndicator(False)

        debugInfo = wx.StaticText(panelLeft,-1,'This is for debug information')
        debugInfo.SetOwnForegroundColour(green)

        vbox.Add(autoPlayButton, 1, wx.EXPAND | wx.ALIGN_TOP)
        vbox.Add(stepButton, 1, wx.EXPAND | wx.ALIGN_TOP)
        vbox.Add(resetButton, 1, wx.EXPAND | wx.ALIGN_TOP)
        vbox.Add(debugInfo, 5, wx.EXPAND | wx.ALIGN_TOP | wx.TOP, 5)

        panelLeft.SetSizer(vbox)
        #END ADD BUTTONS

        #CREATE RIGHT PANEL AND ASTEROID GRID
        panelInsideRight = wx.Panel(panelRight)
        panelInsideRight.SetBackgroundColour(black)
        panelInsideRight.SetFont(wx.Font(20,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        hboxInsideRight = wx.BoxSizer(wx.VERTICAL)
        hboxInsideRight.Add(panelInsideRight,wx.ID_ANY, wx.EXPAND | wx.ALL, 2)
        panelRight.SetSizer(hboxInsideRight)

        num_rows = len(self.grid)
        num_columns = len(self.grid[0])

        gridArray = []

        for rows in range(0,num_rows):
            for columns in range(0,num_columns):
                text = buttons.GenButton(panelInsideRight,-1,self.grid[rows][columns])
                #text.Enable(False)
                text.SetBezelWidth(0)
                text.SetOwnBackgroundColour(black)
                text.SetOwnForegroundColour(green)
                text.SetUseFocusIndicator(False)
                gridArray.append((text,0,wx.EXPAND))
                #print(self.grid[rows][columns])

        asteroidGUI = wx.GridSizer(num_rows,num_columns,0,0)

        asteroidGUI.AddMany(gridArray)

        panelInsideRight.SetSizer(asteroidGUI)


    def initializeGrid(self):

        self.grid = []

        self.grid.append(['#','#','#','#','#','#','#','#','#'])
        self.grid.append(['#','#','#','#','#','#','#','#','#'])
        self.grid.append(['#','#','#','#','#','#','#','#','#'])



def main():

    app = wx.App()
    dayTen = DayTen(None,title="Advent of Code, Day 10")
    dayTen.Show()
    app.MainLoop()



if __name__ =="__main__":
    main()
