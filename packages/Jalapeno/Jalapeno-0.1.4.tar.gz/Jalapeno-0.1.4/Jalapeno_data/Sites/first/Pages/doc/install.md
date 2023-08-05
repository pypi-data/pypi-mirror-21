title: 安装
pos: 1

##安装

在使用Jalapeno之前，我们需要先将所需的软件下载下来。如果已经安装或者电脑上带有，则跳过此环节

- Python3
- pip3(Python3的软件包管理器)
- Jalapeno(我们的博客生成器)
- git(将网页文件部署至Github／Coding)

###Python3/pip3 系列安装

我们在[Python](https://www.python.org/downloads/)的官方网站可以下载对应的版本，最新版本为3.6.0


###终端安装方法

我们以Fedora（Linux）为例

sudo dnf install python3 python3-pip

Ubuntu:

sudo apt-get install python3 python3-pip

Mac:

先安装homwbrew

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    
使用brew(包管理器，类似于dnf/apt)

    brew install python3
    



让我们来测试一下


在终端输入'python3'：

	localhost:pages Jakob$ python3
	
成功进入到Python3的交互界面,注意版本号，当前版本是3.5.1，对我们来说3.4以上的版本最好

	Python 3.5.1 (default, Jan 22 2016, 08:52:08) 
	[GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> 
	
再来看我们的pip3,在终端输入'pip3 -V'查看版本：

	localhost:pages Jakob$ pip3 -V

得到（pip3版本号8以上即可)

	pip 8.0.2 from /usr/local/lib/python3.5/site-packages (python 3.5)

大功告成！来看我们如何安装Jalapeno


###Jalapeno安装

Jalapeno的安装过程十分简单，你只需要在终端执行以下代码即可。如果你遇到无法解决的问题，在这里[提交问题]()，我会尽快作出回应。

	$sudo pip3 install Jalapeno
    
    Collecting Jalapeno
      Downloading Jalapeno-0.0.8.tar.gz (4.5MB)
        100% |████████████████████████████████| 4.5MB 91kB/s 
    Installing collected packages: Jalapeno
      Running setup.py install for Jalapeno ... done
    Successfully installed Jalapeno-0.0.8
    $
    
我们测试一下，直接在终端输入'Jalop',会得到

	ERROR: Not enough or too many parameters. use "Jalop help" or "Jalop -h" for help
	
上面的报错是Jalop执行的结果，我们可以看到Jalop是已经被安装到电脑上的。

