title: 开始一篇博客
pos: 4

###New
现在你准备好了吗？
 
首先我们要在'pages'文件夹下创建一个空白文档'test.md',这里test只是一个名字，你可以给你的文章起任何名字，它将会影响到你未来网页的链接地址：
	
    yourwebsite.com/article/test
  
###Title

接着我们要编辑文档的开头，注意冒号后面要空格

    title: 这里写文章标题
    date: 这里写发表日期，格式为 YYYY-MM-DD 
    tag: 这里是你的文章分类/标签名称
    

###Content

接着我们编写正文，正文要与之前的开头用一个空行隔开

    hello world!balabalabala....
    
    balabalabala....
    
    balabalabala....

###Image

在之前我们提到过图片都放在image文件夹下的文章同名子文件夹下，现在假设我们的testpic.jpg在image/test文件夹下，路径为

    Jalapeno/source/image/test/testimg.jpg
    
我们配合Markdown引用图片的语法:

    \!\[\]\(\图片地址)
    
而我们的图片地址表示方法为

    \{\{image.子文件夹名.图片名}}，

所以最后引用的方法为

    hello world!balabalabala....
    
    \![]({\{image.test.testpic}})
    
    balabalabala....
    
    balabalabala....

    
###Excerpt

如果你想在文章列表中显示摘要，我们使用<!\--More-->来进行分隔。<!\--More-->之前内容会被放到你的文章列表的摘要中

    hello world!balabalabala....
    
    <!\--More-->
    
    balabalabala....
    
    balabalabala....
	
###Sidebar-content

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


###Syntax

想要了解更多Markdown语法，参见[Markdown 语法说明](https://github.com/riku/Markdown-Syntax-CN/blob/master/syntax.md)
    
到这里，我们的博客就写完啦，在发布前我们需要对其测试