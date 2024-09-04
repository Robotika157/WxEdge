# WxEdge
# Version 1.0

import wx
import wx.html2
from datetime import datetime
import urllib.parse

class MainWindow(wx.Frame):
    def __init__(self):
        self.WriteToLogBegin()
        self.WriteToLog(f"[ACTION TAKEN] - __init__ - TYPE: INIT")
        super(MainWindow, self).__init__(None, title="WxEdge 1.0")
        self.home_page = "https://google.com"
        self.fullscreen = False
        self.logtxt = ""

        self.InitUI()

    def InitUI(self):
        self.WriteToLog(f"[ACTION TAKEN] - InitUI - TYPE: INIT")
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Toolbar Setup
        toolbar = wx.ToolBar(panel)
        toolbar.SetToolBitmapSize((16, 16))

        back_bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR, (16, 16))
        back_btn = toolbar.AddTool(wx.ID_ANY, "Back", back_bitmap)
        self.Bind(wx.EVT_TOOL, self.OnBack, back_btn)

        forward_bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, (16, 16))
        forward_btn = toolbar.AddTool(wx.ID_ANY, "Forward", forward_bitmap)
        self.Bind(wx.EVT_TOOL, self.OnForward, forward_btn)

        reload_bitmap = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, (16, 16))
        reload_btn = toolbar.AddTool(wx.ID_ANY, "Reload", reload_bitmap)
        self.Bind(wx.EVT_TOOL, self.OnReload, reload_btn)

        home_bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_TOOLBAR, (16, 16))
        home_btn = toolbar.AddTool(wx.ID_ANY, "Home", home_bitmap)
        self.Bind(wx.EVT_TOOL, self.OnHome, home_btn)

        # New Tab Button
        new_tab_bitmap = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        new_tab_btn = toolbar.AddTool(wx.ID_ANY, "New Tab", new_tab_bitmap)
        self.Bind(wx.EVT_TOOL, self.OnNewTab, new_tab_btn)

        # Fullscreen Toggle Button
        fullscreen_bitmap = wx.ArtProvider.GetBitmap(wx.ART_FULL_SCREEN, wx.ART_TOOLBAR, (16, 16))
        fullscreen_btn = toolbar.AddTool(wx.ID_ANY, "Fullscreen", fullscreen_bitmap)
        self.Bind(wx.EVT_TOOL, self.OnToggleFullscreen, fullscreen_btn)

        toolbar.AddStretchableSpace()
        toolbar.Realize()

        vbox.Add(toolbar, flag=wx.EXPAND | wx.ALL, border=5)

        # Create Notebook for Tabs
        self.notebook = wx.Notebook(panel)
        vbox.Add(self.notebook, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)

        self.CreateStatusBar()

        self.SetSize((800, 600))
        self.Center()

        # Add the first tab
        self.AddNewTab()

    def AddNewTab(self, url=None):
        self.WriteToLog(f"[ACTION TAKEN] - AddNewTab - TYPE: ACTION")
        """Adds a new tab with a browser instance."""
        tab_panel = wx.Panel(self.notebook)
        tab_vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        url_bar = wx.TextCtrl(tab_panel, style=wx.TE_PROCESS_ENTER)
        hbox.Add(url_bar, proportion=1, flag=wx.EXPAND)

        tab_vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)

        # Create browser for the tab
        browser = wx.html2.WebView.New(tab_panel)
        tab_vbox.Add(browser, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        tab_panel.SetSizer(tab_vbox)

        # Bind the URL bar to navigation events
        url_bar.Bind(wx.EVT_TEXT_ENTER, lambda event, browser=browser, url_bar=url_bar: self.OnNavigate(event, browser, url_bar))

        # Bind browser navigation event
        browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, lambda event, url_bar=url_bar: self.OnNavigated(event, url_bar))

        # Bind right-click event to open links in a new tab
        browser.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, self.OnNewWindow)

        # Bind right-click context menu
        browser.Bind(wx.EVT_CONTEXT_MENU, self.OnShowContextMenu)

        # Add the tab with a simple label
        self.notebook.AddPage(tab_panel, "New Tab", select=True)

        # Load the home page or a specified URL
        if url:
            browser.LoadURL(url)
        else:
            browser.LoadURL(self.home_page)

    def OnCloseTab(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnCloseTab - TYPE: ACTION")
        """Handles tab close events from the context menu."""
        if self.notebook.GetPageCount() > 1:
            self.notebook.DeletePage(self.notebook.GetSelection())

    def OnBack(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnBack - TYPE: ACTION")
        browser = self.GetCurrentBrowser()
        if browser and browser.CanGoBack():
            browser.GoBack()

    def OnForward(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnForward - TYPE: ACTION")
        browser = self.GetCurrentBrowser()
        if browser and browser.CanGoForward():
            browser.GoForward()

    def OnReload(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnReload - TYPE: ACTION")
        browser = self.GetCurrentBrowser()
        if browser:
            browser.Reload()

    def OnHome(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnHome - TYPE: ACTION")
        browser = self.GetCurrentBrowser()
        if browser:
            browser.LoadURL(self.home_page)

    def OnNavigate(self, event, browser, url_bar):
        self.WriteToLog(f"[ACTION TAKEN] - OnNavigate - TYPE: ACTION")
        url = url_bar.GetValue()

        # Check if "devtools" was entered
        if url.lower() == "dev://devtools":
            self.OnDeveloperTools(None)
        else:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url  # Prepend http:// if protocol is missing
            if browser:
                browser.LoadURL(url)

    def OnNavigated(self, event, url_bar):
        self.WriteToLog(f"[ACTION TAKEN] - OnNavigated - TYPE: ACTION")
        url = event.GetURL()
        url_bar.SetValue(url)
        self.WriteToLogUrl(url)

    def OnNewTab(self, event=None):
        self.WriteToLog(f"[ACTION TAKEN] - OnNewTab - TYPE: ACTION")
        self.AddNewTab()

    def OnToggleFullscreen(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnToggleFullScreen - TYPE: ACTION")
        self.fullscreen = not self.fullscreen
        self.ShowFullScreen(self.fullscreen)

    def OnNewWindow(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnNewWindow - TYPE: ACTION")
        """Handles opening a new window (tab) from a link."""
        url = event.GetURL()
        self.AddNewTab(url)

    def OnShowContextMenu(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnShowContextMenu - TYPE: ACTION")
        """Shows context menu for right-click events in the browser."""
        menu = wx.Menu()
        open_in_new_tab = menu.Append(wx.ID_ANY, "Open in New Tab")
        close_tab = menu.Append(wx.ID_ANY, "Close Tab")
        
        self.Bind(wx.EVT_MENU, self.OnOpenLinkInNewTab, open_in_new_tab)
        self.Bind(wx.EVT_MENU, self.OnCloseTab, close_tab)

        # Position the menu at the right-click position
        pos = event.GetPosition()
        self.PopupMenu(menu, pos)
        menu.Destroy()

    def OnOpenLinkInNewTab(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - OnOpenLinkInNewTab - TYPE: ACTION")
        """Opens a link in a new tab from the context menu."""
        browser = self.GetCurrentBrowser()
        if browser:
            url = browser.GetCurrentURL()
            self.AddNewTab(url)

    def OnDeveloperTools(self, event):
        self.WriteToLog(f"[ACTION TAKEN] - DevTools Opened - TYPE: ACTION")
        """Opens a simple Developer Tools window."""
        browser = self.GetCurrentBrowser()
        if browser:
            dev_window = DeveloperToolsWindow(self, browser)
            dev_window.Show()

    def GetCurrentBrowser(self):
        """Returns the browser instance of the currently selected tab."""
        current_tab = self.notebook.GetCurrentPage()
        if current_tab:
            # Assuming the WebView is the second child in the vertical box sizer
            return current_tab.GetChildren()[1]  # Get the WebView from the panel
        return None
    def WriteToLog(self, logtxt):
        now = datetime.now()
        formatted_now = now.strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:  # Use 'w' to overwrite the file or 'a' to append to it
            self.logtxt = logtxt
            file.write(f"{self.logtxt} at {formatted_now}\n")  # Writing the first line
    def WriteToLogBegin(self):
        now = datetime.now()
        formatted_now = now.strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:  # Use 'w' to overwrite the file or 'a' to append to it
            file.write("________________________________________________________________________________________________\n")
            file.write(f"NEW SESSION OPENED AT {formatted_now} (D:M:Y H:M:S)\n")
    def WriteToLogUrl(self, urltxt):
        def process_url(urltxtt):
            global search_query
            global prpa
            # Parse the URL
            parsed_url = urllib.parse.urlparse(urltxtt)
    
            # Check if the path starts with '/search'
            if parsed_url.netloc == 'www.google.com' and parsed_url.path == '/search':
                # Parse the query parameters
                query_params = urllib.parse.parse_qs(parsed_url.query)
        
                # Extract the search query (q parameter)
                search_query = query_params.get('q', [''])[0]
                # Print "Search" with the search query
                prpa = 1
            else:
                # Print the original URL
                prpa = 0
        now = datetime.now()
        formatted_now = now.strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:  # Use 'w' to overwrite the file or 'a' to append to it
            process_url(urltxt)
            if prpa == 1:
                file.write(f"SEARCHED '{search_query}' ATTT {formatted_now}\n")
            else:
                file.write(f"VISITED '{urltxt}' AT {formatted_now}\n")

class DeveloperToolsWindow(wx.Frame):
    def __init__(self, parent, browser):
        super(DeveloperToolsWindow, self).__init__(parent, title="Developer Tools", size=(600, 400))
        self.browser = browser
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Text control to display page source
        self.source_view = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.source_view, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Button to view page source
        btn_view_source = wx.Button(panel, label="View Page Source")
        btn_view_source.Bind(wx.EVT_BUTTON, self.OnViewSource)
        vbox.Add(btn_view_source, flag=wx.EXPAND | wx.ALL, border=5)

        # Button to view console logs (if any)
        btn_console_logs = wx.Button(panel, label="View Console Logs")
        btn_console_logs.Bind(wx.EVT_BUTTON, self.OnViewConsoleLogs)
        vbox.Add(btn_console_logs, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)
    
    def WriteToLogDEVMENU(self, logtxt):
        now = datetime.now()
        formatted_now = now.strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a") as file:  # Use 'w' to overwrite the file or 'a' to append to it
            self.logtxt = logtxt
            file.write(f"{self.logtxt} at {formatted_now}\n")  # Writing the first line

    def OnViewSource(self, event):
        self.WriteToLogDEVMENU(f"[ACTION TAKEN - DEVTOOLS MENU] - ViewSource - TYPE: ACTION")
        """Displays the page source code."""
        source = self.browser.GetPageSource()
        self.source_view.SetValue(source)

    def OnViewConsoleLogs(self, event):
        self.WriteToLogDEVMENU(f"[ACTION TAKEN - DEVTOOLS MENU] - ShowConsoleLogs - TYPE: ACTION")
        """Displays console logs (if any)."""
        # wx.html2.WebView doesn't support real-time console logs directly.
        # This is a placeholder function. In practice, you may need to integrate
        # a custom logging mechanism to capture JS console logs.
        with open('log.txt', 'r') as file:
            content = file.read()
            logs = content
        self.source_view.SetValue(logs)

if __name__ == '__main__':
    app = wx.App()
    main_window = MainWindow()
    main_window.Show()
    app.MainLoop()
