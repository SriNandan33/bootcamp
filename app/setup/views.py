from flask import render_template, request, flash,\
    redirect, url_for, current_app
from werkzeug.urls import url_parse
import os
from app import db
from app.setup import bp
from app.models import User
from app.setup.forms import SetupForm
import os


@bp.route('/setup', methods=["GET", "POST"])
def setup():
    form = SetupForm()

    if request.method == "GET":
        if not os.path.isfile(".setupcompleted"):
            return render_template("setup/setup.html", title="Bootcamp - Setup", form=form)
        else:
            return redirect(url_for("auth.login"))

    elif request.method == "POST":
        if not os.path.isfile(".setupcompleted"):
            if form.validate_on_submit():
                env_Vars = {}
                current_app.config.update(
                    MAIL_SERVER=form.mail_server.data,
                    MAIL_PORT=str(form.mail_port.data),
                    MAIL_USE_TLS=str(int(form.mail_use_tls.data)),
                    MAIL_USERNAME = form.mail_username.data,
                    MAIL_PASSWORD = form.mail_password.data,
                    SECRET_KEY = form.secret_key.data,
                    ADMIN_EMAIL = form.admin_email.data,
                    PUSHER_APP_ID = form.pusher_app_id.data,
                    PUSHER_KEY = form.pusher_key.data,
                    PUSHER_SECRET = form.pusher_secret.data,
                    PUSHER_CLUSTER = form.pusher_cluster.data
                )

                env_Vars['FLASK_APP'] = os.environ.get("FLASK_APP")
                env_Vars['MAIL_SERVER'] = form.mail_server.data
                env_Vars['MAIL_PORT'] = str(form.mail_port.data)
                env_Vars['MAIL_USE_TLS'] = str(int(form.mail_use_tls.data))
                env_Vars['MAIL_USERNAME'] = form.mail_username.data
                env_Vars['MAIL_PASSWORD'] = form.mail_password.data
                env_Vars['SECRET_KEY'] = form.secret_key.data
                env_Vars['ADMIN_EMAIL'] = form.admin_email.data
                env_Vars['PUSHER_APP_ID'] = form.pusher_app_id.data
                env_Vars['PUSHER_KEY'] = form.pusher_key.data
                env_Vars['PUSHER_SECRET'] = form.pusher_secret.data
                env_Vars['PUSHER_CLUSTER'] = form.pusher_cluster.data

                print('Setup successful!')
                with open(".setupcompleted", "w+") as f:
                    f.write("")

                with open(".flaskenv", "w") as f:
                    for k,v in env_Vars.items():
                        f.write(k+"="+v+"\n")
            else:
                for fieldName, errorMessages in form.errors.items():
                    print(fieldName, errorMessages)

                flash("Setup Failed!")

            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("auth.login"))