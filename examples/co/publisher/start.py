import wx
import pyperclip
import urllib2
import urllib
import encode
import streaminghttp
import json
TRAY_TOOLTIP = 'Click to send screenshot'
TRAY_ICON = 'icon.png'
LOAD_ICON = 'load.png'
URL = 'http://blog.symfony.com.ua/add'
URL_IMAGE = 'http://blog.symfony.com.ua/image'
TOPIC = 8

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

def get_settings():
    with open('settings.dat') as data_file:    
        data = json.load(data_file)   
    return data

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        
    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Send text', self.send_text)
        create_menu_item(menu, 'Send screenshot', self.send_screenshot)
        create_menu_item(menu, 'Settings', self.show_settings)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        spam = pyperclip.paste()
        self.send_text(self)
        print 'Tray icon was left-clicked.'+str(spam)

    def send_screenshot(self, event):
        import time
        settings = get_settings()
        #t = time.strftime("%I%M%S")
        t = 'temp'
        print t
        time.sleep(1)
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        bmp.SaveFile(t+'.png', wx.BITMAP_TYPE_PNG)

        opener = streaminghttp.register_openers()
        params = {'image': open(t+'.png','rb'), 'lesson': settings['id']}
        datagen, headers = encode.multipart_encode(params)
        response = opener.open(urllib2.Request(settings['url2'], datagen, headers))

        print 'Hello, world!'

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)

    def send_text(self,event):
        frame = ExampleFrame(None)
        frame.Show()

    def show_settings(self,event):
        frame = SettingFrame(None)
        frame.Show()


class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.control1 = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.control1.AppendText(pyperclip.paste())
        self.control2 = wx.Button(self, wx.ID_OK, "Send")
        self.control2.Bind(wx.EVT_BUTTON, self.on_submit)
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer1.Add(self.control1, 1, wx.EXPAND)
        self.sizer1.Add(self.control2, 1, wx.EXPAND)
        self.SetSizer(self.sizer1)
    def on_submit(self,e):
        settings = get_settings()
        txt = self.control1.GetValue()
        self.control1.AppendText('')
        #import pdb; pdb.set_trace()
        txt = txt.encode('utf-8')
        data = {'content': txt,'topic':settings['id']}
        data = urllib.urlencode(data)
        #print ("requesting"+data['url1'])
        urllib2.urlopen(settings['url1'], data)
        #import pdb; pdb.set_trace
        print self.control1.GetValue()
        #self.Hide()

class SettingFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.url1 = wx.TextCtrl(self, 1, size=(20, -1))
        self.url2 = wx.TextCtrl(self)
        self.id = wx.TextCtrl(self)
        data = get_settings()
        self.url1.AppendText(data['url1'])
        self.url2.AppendText(data['url2'])
        self.id.AppendText(data['id'])
        self.button = wx.Button(self, wx.ID_OK, "Save")
        self.button.Bind(wx.EVT_BUTTON, self.save_settings)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.url1, 1, wx.EXPAND)
        self.sizer.Add(self.url2, 1, wx.EXPAND)
        self.sizer.Add(self.id, 1, wx.EXPAND)
        self.sizer.Add(self.button, 1)
        self.SetSizer(self.sizer)
    def save_settings(self,e):
        data = {'url1':self.url1.GetValue(),'url2': self.url2.GetValue(),'id': self.id.GetValue()}
        with open('settings.dat', 'w') as outfile:
            json.dump(data, outfile)
        self.Hide()


def main():
    app = wx.PySimpleApp()
    TaskBarIcon()

    app.MainLoop()



if __name__ == '__main__':
    main()


