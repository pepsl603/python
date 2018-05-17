import wx


class MyApp(wx.App):
    def OnInit(self):
        window = wx.Frame(parent=None, title='Hello', pos=(500, 300), size=(400, 300))
        panel = wx.Panel(window)
        label = wx.StaticText(panel, label='你好，窗口来了', pos=(100, 100))
        window.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
