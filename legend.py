#!/usr/bin/env python2

import wx
import time

TRAY_TOOLTIP = 'Personal Legend'
TRAY_ICONS = {
    'main': 'icon-main.png',
    'c1': 'icon-1card.png',
    'c2': 'icon-2cards.png',
    'c3': 'icon-3cards.png',
    'timer': 'icon-zero.png'
}
TRAY_TIMER = 30 * 60

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_status('main')
        self.timer = 0
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Timer', self.stop_watch)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def set_status(self, st):
        self.set_icon(TRAY_ICONS[st])
        self.status = st

    def on_left_down(self, event):
        if self.status == 'main':
            self.set_status('c1')
        elif self.status == 'c1':
            self.set_status('c2')
        elif self.status == 'c2':
            self.set_status('c3')
        elif self.status == 'c3':
            self.set_status('main')

    def on_hello(self, event):
        print('Hello, world!')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)

    def stop_watch(self, event):
        now = time.time()
        future = now + TRAY_TIMER
        self.timer = 0
        self.set_icon('icon-zero.png')
        while now < future:
            i = 10 - int(10*(future - now)/TRAY_TIMER + 0.8)
            if i > self.timer:
                self.timer = self.timer + 1
                self.set_icon('icon-t' + str(i) + '.png')
            time.sleep(0.1)
            wx.Yield()
            now = time.time()
            pass

def main():
    #app = wx.PySimpleApp()
    app = wx.App(False)
    TaskBarIcon()
    app.MainLoop()


if __name__ == '__main__':
    main()
