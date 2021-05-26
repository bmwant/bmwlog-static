---
title: Creating desktop screenshots with Python
date: 2020-03-05 11:29:52
tags: [python, qt, opencv, image]
author: Misha Behersky
---

In this article I'm going to show how to accomplish a simple task of creating a screenshot using various Python tools. Alongside we'll see other useful methods of working with pictures. Let's start with the simplest way possible.

We'll be using [pyscreenshot](https://github.com/ponty/pyscreenshot) package `pip install pyscreenshot`
```python
import pyscreenshot

im = pyscreenshot.grab()

# save image file
im.save('screenshot1.png')

# show image in a window
im.show()
```

Three lines of code (importing/instantiating/saving). Is there anything easier than that? Actually, pyscreenshot is a wrapper around various backends, so to make it work you have to have at least one of it installed. `pip install Pillow` will work for this example by using popular Python fork for [PIL](https://www.pythonware.com/products/pil/) called [Pillow](https://github.com/python-pillow/Pillow).

### PyAutoGui
[PyAutoGUI](https://github.com/asweigart/pyautogui) is really powerful module for automation. It's capable of moving your mouse, control keyboard and handle user inputs. It also has a handy way of creating a screenshot but basically it's again a wrapper around Pillow. So go with `pip install pyautogui` and add another three simple lines of code

```python
import pyautogui

im = pyautogui.screenshot()
im.save('screenshot2.png')
```

### PyQt

[PyQt](https://www.riverbankcomputing.com/software/pyqt/intro) is even more powerful toolkit allowing you to create complex GUI applications. It's a set of binding for [Qt](https://en.wikipedia.org/wiki/Qt_(software)) framework which Python users can utilize. The program will be a little longer because you need to instantiate your application object but really you might want to use this snippet only if you already have some code written PyQt or plan to develop graphical application. As usually we start by installing package with `pip install pyqt5`. There is an older version PyQt4, so make sure you didn't accidentally install that because they are not totally compatible and you should be using newer release.

```python
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen

app = QApplication(sys.argv)
im = QScreen.grabWindow(
    app.primaryScreen(),
    QApplication.desktop().winId()
)
im.save('screenshot3.png')
```

### wxPython?

If for some reason you happen to use [wxPython](https://wxpython.org/) there is a recipe for you as well.

```python
import wx

app = wx.App(False)
screen = wx.ScreenDC()

size = screen.GetSize()
width = size.width
height = size.height
bmp = wx.Bitmap(width, height)

# Create a memory DC that will be used for actually taking the screenshot
memDC = wx.MemoryDC()
# Tell the memory DC to use our Bitmap
# all drawing action on the memory DC will go to the Bitmap now
memDC.SelectObject(bmp)
# Blit (in this case copy) the actual screen on the memory DC
memDC.Blit(
    0, 0,
    width, height,
    screen,
    0, 0
)
# Select the Bitmap out of the memory DC by selecting a new bitmap
memDC.SelectObject(wx.NullBitmap)
im = bmp.ConvertToImage()
im.SaveFile('screenshot4.png', wx.BITMAP_TYPE_PNG)
```

The only important note is that you should install/build your Python distribution [with framework support enabled](https://github.com/pyenv/pyenv/wiki#how-to-build-cpython-with-framework-support-on-os-x). With [pyenv](https://github.com/pyenv/pyenv) it's simple as the following

```bash
$ export PYTHON_CONFIGURE_OPTS="--enable-framework"
$ pyenv install 3.7.6
```

Otherwise you might get annoying error which prevents you from running the code, error message example from my laptop below

```
This program needs access to the screen. Please run with a
Framework build of python, and only when you are logged in
on the main display of your Mac.
```

### Cropping a screenshot

Usually you are interested in some specific region of the image (called ROI/box) not the fullscreen. Here's couple of method how that can be done. First one does the job with OpenCV `pip install opencv-contrib-python`

```python
import cv2

im = cv2.imread('screenshot.png')
# initial point
x = 0
y = 0
# size of the resulting image
height = 200
width = 400
cropped = im[y:y + height, x:x + width]
cv2.imwrite('cropped.png', cropped)
```

Note that `x` and `y` indexing within `im` is swapped here, so double-check your code.

Second method use Qt

```python
from PyQt5.QtCore import QRect, QPoint, QSize

height = 200
width = 400
roi = QRect(
    QPoint(10, 10),
    QSize(width, height)
)
cropped = im.copy(roi)
cropped.save('cropped.png')
```

You can also omit using `QPoint` and `QSize` structures and pass numbers as arguments directly

```python
x = 0
y = 0
height = 200
width = 400
roi = QRect(
    x, y,
    width, height
)
```

or even `cropped = im.copy(x, y, width, height)`.

I hope with such variety of methods everybody will be able to find approach to fit their toolset. Happy coding and see you soon.

### Resources
* [Documentation for pyscreenshot](https://pyscreenshot.readthedocs.io/en/latest/)
* [Pillow documentation](https://pillow.readthedocs.io/en/stable/)
* [PyAutoGUI documentation](https://pyautogui.readthedocs.io/en/latest/)
* [Related StackOverflow question](https://stackoverflow.com/questions/10705712/screenshot-of-a-window-using-python/60020534)
* [Installing opencv on different platforms](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)
* [How to use pyenv](https://bmwlog.pp.ua/post/using-pyenv-on-ubuntu)
