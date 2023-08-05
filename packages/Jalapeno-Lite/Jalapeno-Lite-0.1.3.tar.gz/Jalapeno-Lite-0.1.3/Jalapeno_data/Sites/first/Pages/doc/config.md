title: 初始化&配置
pos: 2

###初始化Jalapeno目录

首先我们在终端执行

    $Jalop -s

或
 
    $Jalop shortcuts
    
该指令可以在你的用户主目录（下载／文档／图片／...的上一级目录）下生成一个'Jalapeno'文件夹，但是你的文件夹上面会有一把锁子的图标，意味着你的文件夹需要访问权限，需要输入密码才能修改，你可能会说这多不方便啊。于是我们有了下面的操作，把这把锁子去掉

    
    $Jalop -u
或

    $Jalop unlock
    
好了，来看我们的目录文件夹吧。

###配置个人信息

在第一次运行前我们需要对Jalapeno进行简单的配置，例如你的个人信息什么的，在我们生成的Jalapeno文件夹的Profile子文件夹中有一个'profile.yaml'文件，用编辑器打开它，找到并修改以下内容

    Name: 我的博客
    Motto: 你总有一个坚持下去的理由
    Github: https://github.com/ChenghaoQ
    copyright: 版权归ChenghaoQ所有

除此之外，本主题含有的页面头像对应Jalapeno/source/image/theme/Selfie.jpg,如果需要更改使用其他文件替换即可

效果展示


