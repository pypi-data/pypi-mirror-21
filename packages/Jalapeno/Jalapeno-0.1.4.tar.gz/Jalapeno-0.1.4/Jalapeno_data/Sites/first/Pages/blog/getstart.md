title: 使用Jalapeno快速搭建博客
date: 2017-01-19
tag: Flask

[TOC]

<!--Sidebar-->

上次我们讲了如何使用Flask系列来搭建静态博客，但是实际上功能仍然比较单一。为了省去大家重复造轮子的辛苦，老钱同志在今年年初发布了Jalapeno。由于偷懒原因（逃），官方文档一直未能发布。这次我们讲如何使用Jalapeno快速搭建自己的博客网站。

![]({{image.getstart.init}})

注：Jalapeno当前支持Mac/Linux， Windows目前尚未测试。

<!--More-->

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




##初始化Jalapeno目录

首先我们在终端执行

    $Jalop -s

或
 
    $Jalop shortcuts
    
该指令可以在你的用户主目录（下载／文档／图片／...的上一级目录）下生成一个'Jalapeno'文件夹，但是你的文件夹上面会有一把锁子的图标，意味着你的文件夹需要访问权限，需要输入密码才能修改，你可能会说这多不方便啊。于是我们有了下面的操作，把这把锁子去掉

    
    $Jalop -u
或

    $Jalop unlock
    
好了，来看我们的目录文件夹吧。
    
![]({{image.getstart.shortcutdir}})
##Jalapeno目录介绍
我们来看一下新的Jalapeno文件夹目录构成

    Jalapeno
    ├── Profile
    |      └── profile.yaml 
    |
    ├── build 
    ├── source
    |     ├── pages
    |     └──  image

	
Jalapeno由三个文件夹构成，其中

- Profile存放配置文件及个人信息，目前版本所有信息存放于profile.yaml
- source 存放文档及资源文件
    - pages存放文档，你将来写的博客文章存放在这里
    - image存放图片，将来所有的图片都将存放在这里，建议大家在image中创建于文章名对应的文件夹并将图片放入其中，比如目前我们有一篇文章名字为test.md,我们就在image下创建test文件夹，并将test.md中使用的图片放在该目录下
	

##配置Jalapeno

在第一次运行前我们需要对Jalapeno进行简单的配置，例如你的个人信息什么的，在我们生成的Jalapeno文件夹的Profile子文件夹中有一个'profile.yaml'文件，用编辑器打开它，找到并修改以下内容

    Name: 我的博客
    Motto: 你总有一个坚持下去的理由
    Github: https://github.com/ChenghaoQ
    copyright: 版权归ChenghaoQ所有

除此之外，本主题含有的页面头像对应Jalapeno/source/image/theme/Selfie.jpg,如果需要更改使用其他文件替换即可

效果展示

![]({{image.getstart.desktop}})



##开始一篇博客
 
现在你准备好了吗？
 
首先我们要在'pages'文件夹下创建一个空白文档'test.md',这里test只是一个名字，你可以给你的文章起任何名字，它将会影响到你未来网页的链接地址：
	
    yourwebsite.com/article/test
    
接着我们要编辑文档的开头，注意冒号后面要空格

    title: 这里写文章标题
    date: 这里写发表日期，格式为 YYYY-MM-DD 
    tag: 这里是你的文章分类/标签名称
    
接着我们编写正文，正文要与之前的开头用一个空行隔开

    hello world!balabalabala....
    
    balabalabala....
    
    balabalabala....
    
在之前我们提到过图片都放在image文件夹下的文章同名子文件夹下，现在假设我们的testpic.jpg在image/test文件夹下，路径为

    Jalapeno/source/image/test/testimg.jpg
    
我们配合Markdown引用图片的语法:

    \!\[\]\(\图片地址)
    
而我们的图片地址表示方法为

    \{\{image.子文件夹名.图片名}}，

所以最后引用的方法为

    hello world!balabalabala....
    
    \!\[]\(\{\{image.test.testpic}})
    
    balabalabala....
    
    balabalabala....

    
	
如果你想在文章列表中显示摘要，我们使用<!\--More-->来进行分隔。<!\--More-->之前内容会被放到你的文章列表的摘要中

    hello world!balabalabala....
    
    <!\--More-->
    
    balabalabala....
    
    balabalabala....
	
	
如果你想在你的文章中启用索引/目录，我们使用\[TOC\]作为标示，将\[TOC\]放入你希望的位置，Jalapeno会在该位置生成目录。前提是你有使用'\#'号来注明各个子标题


    \[TOC\]

    hello world!balabalabala....
    
    <!\--More-->
    
    ##第一个标题
    
    balabalabala....
    
    ##第二个标题
    
    balabalabala....
	
	
如果你想将目录放入侧边栏而不是正文，我们使用<!\--Siderbar-->进行标记，<!\--Siderbar-->上面的内容会被放入侧边栏目录中，注意，与\[TOC\]用空行隔开


    \[TOC\]

    <!\--Siderbar-->

    hello world!balabalabala....
    
    <!\--More-->
    
    ##第一个标题
    
    balabalabala....
    
    ##第二个标题
    
    balabalabala....
	
想要了解更多Markdown语法，参见[Markdown 语法说明](https://github.com/riku/Markdown-Syntax-CN/blob/master/syntax.md)
    
到这里，我们的博客就写完啦，在发布前我们需要对其测试


##本地测试

    $Jalop -r
    
    
    $Jalop run
	
终端显示

    localhost:~ Jakob$ Jalop run
     * Running on http://127.0.0.1:9999/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger pin code: 111-037-567
     ...
     
这时打开浏览器，进入127.0.0.1:9999，就可以看到我们的网站啦

预览效果


![]({{image.getstart.desktop1}})
![]({{image.getstart.preview}})
![]({{image.getstart.preview1}})
![]({{image.getstart.preview2}})
![]({{image.getstart.preview3}})



##网页生成

当我们在测试服务器上确认网页运行正常后，我们将要生成网页

执行

    $Jalop -f
    
或

    $Jalop freeze
    

生成后就可以看到我们生成的网页啦。

![]({{image.getstart.freeze}})



##部署

    
接着我们将生成的网页部署在

- 自己的服务器上

或托管在免费的

- [Github pages](https://pages.github.com)
- [Coding pages](https://coding.net/help/doc/pages/)

上.详细方法点击链接参见说明文档。过程很简单，就是将生成的文件上传至指定位置即可。



