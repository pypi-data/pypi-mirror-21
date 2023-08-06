Whisper & Message - 私信会话和私信消息
======================================

..  topic:: 注意

    请先查看 :doc:`说明 <intro>` 了解一下知乎相关类的文档的阅读方法。
    否则你会看不懂下面的东西的…………

Example - 用法示例
------------------

..  code-block:: python

    # 省略登录步骤

    me = client.me()

    for whisper in me.whispers:
        print("Whisper with", whisper.who.name)
        print('Allow_reply', whisper.allow_reply)
        print('Unread count', whisper.unread_count)
        print('Updated time', whisper.updated_time)
        print('Snippet', whisper.snippet)
        print('-------------------------------------')
        for message in whisper.messages:
            print(message.format("{sender} to {receiver}: {content}")
        print('-------------------------------------')


Class Ref - 类文档
------------------

..  automodule:: zhihu_oauth.zhcls.whisper
    :members:
    :undoc-members:

..  automodule:: zhihu_oauth.zhcls.message
    :members:
    :undoc-members:
