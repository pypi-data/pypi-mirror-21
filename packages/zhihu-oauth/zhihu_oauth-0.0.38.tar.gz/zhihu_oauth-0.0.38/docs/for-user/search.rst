Search - 搜索
-------------

知乎的搜索功能通过 :any:`ZhihuClient.search` 方法提供。

目前知乎提供了 6 个搜索方式， :any:`SearchType` 枚举常量表示这六种方式，作为参数传递给 :any:`ZhihuClient.search` 方法。

方式与枚举常量对应关系如下：

..  automodule:: zhihu_oauth.zhcls.search
    :members: SearchType

搜索的常见用法：

..  code-block:: Python

    client.search('程序', SearchType.COLUMN)
    client.search('7sDream', SearchType.PEOPLE)

除了 ``SearchType.GENERAL`` 方式，其他方式的搜索都会返回 :any:`SearchResult` 对象的迭代器。

可用属性如下：

..  autoclass:: zhihu_oauth.zhcls.search.SearchResult
    :members:
    :undoc-members:
    :special-members: __init__

所以一般这样用：

..  code-block:: Python

    for result in client.search('程序', SearchType.COLUMN):
        column = result.obj
        print(column.title, column.author.name)
        # do something with `column`

结果： ::

    程序员实验室 Wayne Shi
    程序员达达 达达
    程序人生 hi大头鬼hi
    程序员的自我修养 luckystar
    反转程序猿 大房
    程序员作战手册 Jim Jin
    红客联盟 小食妹
    非著名程序员 loonggg

其他类型的搜索的用法也类似，就不赘述了。

而 ``SearchType.GENERAL`` 方式的搜索也是迭代器，但可能返回 :any:`SearchResult` 和 :any:`SearchResultSection` 对象。
:any:`SearchResultSection` 对象除了自身有一些属性（见下）之外，本身也是个 :any:`SearchResult` 的迭代器：

..  autoclass:: zhihu_oauth.zhcls.search.SearchResultSection
    :members:
    :special-members: __init__

这样用起来就有点麻烦，你得判断迭代器返回的是那种对象，大概就要这样写：

..  code-block:: Python

    for result in client.search("panda", search_type=SearchType.GENERAL):
        if isinstance(result, SearchResultSection):
            print(result.type, "search result list:")
            for r in result:
                # do something with r
                print(r.obj)
        else:
            # result is SearchResult object
            r = result
            # do something with r
            print(r.highlight_title, r.highlight_desc)
            print(r.obj)
        print('-' * 20)

结果如下： ::

    topic search result list:
    <zhihu_oauth.zhcls.topic.Topic object at 0x7f19e9c1ce48>
    --------------------
    column search result list:
    <zhihu_oauth.zhcls.column.Column object at 0x7f19e9c1ce48>
    --------------------
    people search result list:
    <zhihu_oauth.zhcls.people.People object at 0x7f19e9c1ce48>
    <zhihu_oauth.zhcls.people.People object at 0x7f19e9c1ceb8>
    <zhihu_oauth.zhcls.people.People object at 0x7f19e9c1ce80>
    --------------------
    你有哪些收藏来反复看的<em>大熊猫</em>（<em>panda</em>）的图片？ <em>熊猫</em><em>panda</em>的尾巴是白色的白色的白色的,重说三,看到好多<em>熊猫</em>玩偶都把<em>熊猫</em>尾巴做成黑色的,就连功夫<em>熊猫</em>里阿宝的尾巴都是黑色的,我觉得有必要科普一下哦,对了,图片来自ipanda,
    <zhihu_oauth.zhcls.answer.Answer object at 0x7f19e9c1cef0>
    --------------------
    如何评价<em>熊猫</em>tv狼人杀新节目<em>panda</em>kill？ 10月22日局更新.就第一集而言个人分析仅供参考.首先十二位玩家一一点评.1号鼠大王:比上一季进步了,当民的时候站边,发言都阳光了很多,没有被抗推就是不错的进步,但是当狼的时候依然会紧张状态不稳,第三
    <zhihu_oauth.zhcls.answer.Answer object at 0x7f19e9c1cef0>
    --------------------
    # ... 未完 ...

由于这样写不是很方便，所以提供了 :any:`ZhihuClient.search_unfold` 方法，他会自动将 :any:`SearchResultSection` 展开，生成 :any:`SearchResult` 型的对象，用法：

..  code-block:: Python

    for result in client.search_unfold("panda"):
        # result is SearchResult object
        r = result
        print(r.highlight_title, r.highlight_desc)
        print(r.obj)
        print('-' * 20)


结果： ::


    <zhihu_oauth.zhcls.topic.Topic object at 0x7f6ffa42bf60>
    --------------------
    我吃掉了一辆奔驰
    <zhihu_oauth.zhcls.column.Column object at 0x7f6ffa42bf60>
    --------------------

    <zhihu_oauth.zhcls.people.People object at 0x7f6ffa42bf60>
    --------------------

    <zhihu_oauth.zhcls.people.People object at 0x7f6ffa42bf60>
    --------------------

    <zhihu_oauth.zhcls.people.People object at 0x7f6ffa42bf60>
    --------------------
    你有哪些收藏来反复看的<em>大熊猫</em>（<em>panda</em>）的图片？ <em>熊猫</em><em>panda</em>的尾巴是白色的白色的白色的,重说三,看到好多<em>熊猫</em>玩偶都把<em>熊猫</em>尾巴做成黑色的,就连功夫<em>熊猫</em>里阿宝的尾巴都是黑色的,我觉得有必要科普一下哦,对了,图片来自ipanda,
    <zhihu_oauth.zhcls.answer.Answer object at 0x7f6ffa42bf60>
    --------------------
    如何评价<em>熊猫</em>tv狼人杀新节目<em>panda</em>kill？ 10月22日局更新.就第一集而言个人分析仅供参考.首先十二位玩家一一点评.1号鼠大王:比上一季进步了,当民的时候站边,发言都阳光了很多,没有被抗推就是不错的进步,但是当狼的时候依然会紧张状态不稳,第三
    <zhihu_oauth.zhcls.answer.Answer object at 0x7f6ffa42bef0>
    --------------------
    如何评价11.5 <em>panda</em>kill 各位的表现？ 其实这一期我感觉没有分析的必要,因为这一期总体上就是上一集坏现象进一步恶化后形成的的&quot;进阶版大乱斗&quot;,重复的话我觉得没必要再说了,这里随手放个上一期回答的链接~如何评价10.29 pandakill
    <zhihu_oauth.zhcls.answer.Answer object at 0x7f6ffa42bf28>
    --------------------
    # ... 未完 ... 最前面那些空行是因为 `highlight_title` 和 `highlight_desc` 属性都是空。

推荐在综合搜索时使用 :any:`ZhihuClient.search_unfold` 方法，注意，此方法不支持设置搜索类型，也就是说只支持综合搜索。
