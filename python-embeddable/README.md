# python-embed
python 官方有嵌入式的发行版，不需要安装，开箱即用，而且它占用空间非常小。使用 python-embed 开发程序后再将程序源码和 python-embed 一起打包成可执行文件比 pyinstaller 打包出来的文件要小。
python-embed 不包含pip，不包含tk/tcl，需要另外安装。

## 下载 python-embed
在[官网](https://www.python.org/downloads/)上找到对应平台对应版本的 embeddable zip file 并下载，然后解压，这里将解压得到的文件夹重命名为 python-embed 方便下文描述。

## 安装 pip
- 在 python-embed 目录中找到 pythonxx._pth 文件(xx 指的是 python 版本，如 python3.7 对应的是 python37._pth)
- 下载 [get-pip.py](https://bootstrap.pypa.io/get-pip.py)，保存到 python-embed 目录中
- 在终端中 cd 到 python-embed 目录，执行 `./python.exe get-pip.py`，如果安装成功 python-embed/Scripts 目录中会多出 pip.exe 等文件
- 在终端中 cd 到 python-embed/Scripts 目录，通过执行 `./pip.exe install xxxx` 来安装包

## 安装 tkinter
- 在本地的 python 安装目录中复制多个相关文件和文件夹到 python-embed 目录中，需要的文件和文件夹如下：
    + DLLs 目录下的 _tkinter.pyd，tcl86t.dll， tk86t.dll
    + tcl 目录
    + Lib 目录下的 tkinter 目录

## Templates
这里有几个已经安装好相关文件的项目模板，可以直接下载使用

### [python-3.7.5-pip]( https://github.com/DataYI/ProjectTemplate/tree/master/python-embeddable/python-3.7.5-pip )
已安装好 pip

### [python-3.7.5-pygame]( https://github.com/DataYI/ProjectTemplate/tree/master/python-embeddable/python-3.7.5-pygame )
已安装好 pip 和 pygame

### [python-3.7.5-tkinter]( https://github.com/DataYI/ProjectTemplate/tree/master/python-embeddable/python-3.7.5-tkinter )
已安装好 pip 和 tkinter