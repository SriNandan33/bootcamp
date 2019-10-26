from pusher import Pusher as BasePusher



class Pusher(BasePusher):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        super(Pusher, self).__init__(
            app_id = app.config["PUSHER_APP_ID"],
            key = app.config["PUSHER_KEY"],
            secret = app.config["PUSHER_SECRET"],
            cluster = app.config["PUSHER_CLUSTER"],
            ssl = True
        )
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions["pusher"] = self