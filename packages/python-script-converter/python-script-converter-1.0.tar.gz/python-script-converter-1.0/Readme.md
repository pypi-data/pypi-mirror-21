# **Python-script-converter**

[![PyPI](https://img.shields.io/pypi/v/yagmail.svg?style=flat-square)]()

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)]()

页面下方有中文介绍！

## Introduction:

​	This is a tiny tool used to convert a python script(e.g. demo.py -> demo.command) to a executable file(For mac and Linux),so that you are able to use it anywhere.

## Installation

Tip: Add #!/usr/bin/env python or #!/usr/bin/env python3 in  first line of your script to specify interpreter.So you do not need add python version when you use psc.

### Option 1:Install via pip（Better）

```
$ pip3 install python-script-converter
```

you can also use pip.

### Option 2:Download from Github

You may either download the stable (identical with the latest release on PyPI) or the master branch of you-get. Unzip it, and put the directory containing the you-get script into your PATH.

```
$ [sudo] python3 setup.py install
```

you can also use python.

## Usage:

Before use it, you should ensure:

- You're using Mac OS or Linux.

Here's' how you use `psc`  to create a new executable file base on you original script :

#### If your script based on python3.x

```
$ psc test.py
```

Or use abspath.

```
$ psc /Users/zyh/test.py
```

#### If your script based on python2.x

```
$ psc test.py 2
```

or

```
$ psc /Users/zyh/test.py 2
```

then,you can get a executable file,its name is the same as your script,but its extension is **.command**. and what's more,**it will not change your original script**.

## 介绍：

​	这是一个简单的工具，作用是将一个python脚本直接转换为可执行文件(只供mac和Linux系统使用)。如此，你可以在系统的任何地方运行这个脚本。

## 安装

注:可在你的脚本程序首行加入#!/usr/bin/env python 或者#!/usr/bin/env python3 来指定解释器。这样使用psc时不需要指定版本号。

### Option 1:通过pip安装（推荐）

```
$ pip3 install python-script-converter
```

你也可以使用pip

### Option 2:从Github从下载最新版本

解压下载的zip文件，然后切换到解压后的目录

```
$ [sudo] python3 setup.py install
```

你也可以使用python

## 如何使用：

使用之前，你必须确保：

- 你的系统是Mac OS 或者LInux

下面演示如何使用 `psc`  来将一个脚本转换至可执行程序

#### 如果你的脚本基于python3.x

```
$ psc test.py
```

或者使用绝对路径

```
$ psc /Users/zyh/test.py
```

#### 如果你的脚本基于python2.x

```
$ psc test.py 2
```

or

```
$ psc /Users/zyh/test.py 2
```

之后，你就可以得到一个与脚本名字相同，但是扩展名不同的可执行文件。**程序不会改变你原来的脚本文件**。

