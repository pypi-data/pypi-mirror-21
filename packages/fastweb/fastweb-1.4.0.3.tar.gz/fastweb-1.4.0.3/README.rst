FastWeb Web Server
==================

依赖 ``Tornado`` 开发的快速构建web应用的框架。

示例
----

下面是一个简单的例子:

.. code-block:: python

    import fastweb.API
    import fastweb.UI

    class MainHandler(API):
        def get(self):
            self.write("Hello, world")
            
    class UIModule(UI):
        def render(self):
            self.render_string('index.vm')

    def make_app():
        return tornado.web.Application([
            (r"/", MainHandler),
        ])

    if __name__ == "__main__":
        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()
        
安装
----

``python setup install``