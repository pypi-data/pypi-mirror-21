Activity - 用户动态
===================


..  automodule:: zhihu_oauth.zhcls.activity
    :members:
    :special-members: __init__
    :undoc-members:

辅助函数
--------

因为用户动态比较复杂，我写了几个辅助函数来让开发效率更高。

首先是在获取用户动态的时候，合理利用 :any:`ActivityGenerator.filter` 函数能够快速的获得需要的动态。

另外 :any:`act2str` 和 :any:`ActivityFormatter` 能把一个 :any:`Activity` 转换为字符串描述。
