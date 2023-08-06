一些辅助函数
============

生成器护盾（误
--------------

由于知乎有很多列表型数据，比如用户的关注者，问题的答案，专栏的文章，等等。这些数据在
知乎的 API 里是通过统一的分页逻辑来一段一段的发送的。（详细说明请看：:ref:`generator`）

所以在用 ``for...in loop`` 获取这些数据的时候由于网络或者知乎的原因可能出现异常，
但是因为是生成器，如果你在外部 ``try...catch`` 处理异常的话，就又需要从头开始获取数据了……

所以知乎的分页数据生成器提供了 jump 函数，方便你处理完异常之后跳到上次的地方继续获取数据……（见 :any:`BaseGenerator.jump`）

但是这样还是很麻烦 =。=，所以我写了个辅助函数 shield 来处理这个问题。

如果下面的说明和例子看不懂的话……点开右边的 ``[源代码]`` 按钮，看看源码你就懂了……

..  autofunction:: zhihu_oauth.helpers.shield
..  autodata:: zhihu_oauth.helpers.SHIELD_ACTION

时间戳转换
----------

..  autofunction:: zhihu_oauth.helpers.ts2str


用户动态格式化
--------------

..  autodata:: zhihu_oauth.helpers.act2str
..  autoclass:: zhihu_oauth.helpers.ActivityFormatter
