from pusher import Pusher as BasePusher



class Pusher(BasePusher):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        super(Pusher, self).__init__(
            app_id = app.config["pusher_app_id"],
            key = app.config["pusher_key"],
            secret = app.config["pusher_secret"],
            cluster = app.config["pusher_cluster"],
            ssl = True
        )
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions["pusher"] = self