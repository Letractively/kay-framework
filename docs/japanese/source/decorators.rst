=============================
デコレーター
=============================

.. module:: kay.utils.decorators

ビューデコレーター
=============================

Kay は Appengine 環境での開発に便利なデコレーター関数をいろいろ
揃っています。このデコレーターはよく使えそうな機能を再利用できる
ように実装されています。

.. function:: maintenance_check(endpoint='_internal/maintenance_page')

    ``maintenance_check()`` デコレーターは Appengine データストアが
    メンテナンスモードの状態になっているかを確認し、メンテナンスモード
    の場合、メンテナンス画面にリダイレクトしてくれます。デフォールトは
    '_internal/maintenance_page' という URL ルーティングエンドポイントに
    リダイレクトしますが、 ``endpoint`` という引数で指定することができます。

    ::

        @maintenance_check
        def my_view(request):
            # ...
            return response

.. function:: cron_only()

    ``cron_only()`` デコレーターは Appengine の cron サービスからのリクエストかを
    確認するデコレーターです。適切な HTTP ヘッダーを確認し、 cron リクエストではない場合、
    403 Forbidden リスポンすを返す。しかし、開発の時に便利に使えるため、一つの例外があります。
    :attr:`DEBUG` は `True` で、開発サーバーで動かしている場合は全てのリクエストを通す。
        
    ::

        @cron_only
        def my_cron_view(request):
            # ...
            return response

ユティリティデコレーター
=============================

.. function:: retry_on_timeout(retries=3, secs=1)

    ``retry_on_timeout()`` デコレーターはデータストアにアクセスする処理を
    実行する間にデータストアのAPIタイムアウトが起こった場合、
    数回リトライすることができる。ラップする関数は何回実行されることがあります
    ので、一回以上実行してもシステムが動くように
    `冪等 <http://ja.wikipedia.org/wiki/%E5%86%AA%E7%AD%89>`_
    にしないといけません。

    ::

        @retry_on_timeout(retries=5)
        def my_writer_func():
            # Some datastore operation
            return

.. function:: auto_adapt_to_methods()

    ``auto_adapt_to_methods()`` はデコレーターがメソッドに使っても
    動くようにしてくれるデコレーターのデコレーターです。メソッドの場合、
    self 引数が入ってくるので、普通の関数と違って、特別に扱わないといけない。
    このデコレーターはメソッドをラップしているかを認識して、動的に self 引数
    を扱う。
    
    ::

        @auto_adapt_to_methods
        def my_decorator(func):
            def new_func():
                # ...
                return
            return new_func
