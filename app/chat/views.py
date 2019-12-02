from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app import pusher, db
from app.chat import bp as chat_bp
from app.models import User, Channel, Message


@chat_bp.route("/")
@chat_bp.route("/<username>")
def chat(username=None):
    recipient = None
    if username:
        recipient = User.query.filter_by(username=username).first()
    return render_template("chat/chat.html", recipient=recipient)


@chat_bp.route('/request_chat', methods=["POST"])
@login_required
def request_chat():
    data = request.json
    recipient_id = data["recipient_id"]
    sender_id  = current_user.id
    sender_chat_channel = f"private-chat_user_{sender_id}"
    recipient_chat_channel = f"private-chat_user_{recipient_id}"
    
    # get channel between sender, recipient if exists
    # create otherwise
    channel = Channel.get_or_create(sender_id, recipient_id)

    data = {
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "sender_chat_channel": sender_chat_channel,
        "recipient_chat_channel": recipient_chat_channel,
        "channel_name": channel.name,
        "channel_id": channel.id,
    }
    # trigger an event to recipient
    pusher.trigger(recipient_chat_channel, "new_chat", data)

    return jsonify(data)

@chat_bp.route('/send_message', methods=["POST"])
@login_required
def send_message():
    data = request.json
    sender_id = data["sender_id"]
    recipient_id = data["recipient_id"]
    message = data["message"]
    channel = data["channel"]
    
    channelObj = Channel.query.get(channel)
    new_message = Message(body=message, channel_id=channel)
    new_message.sender_id = sender_id
    new_message.recipient_id = recipient_id
    db.session.add(new_message)
    db.session.commit()

    data["channel_name"] = channelObj.name
    # message html is used in chat box
    # It will have different styles for sender, recipient
    # So We need to render for each user separatly
    data["message"] = render_template("chat/message.html", message=new_message, user_id=recipient_id)
    
    # send the message to recipient via pusher
    pusher.trigger(channelObj.name, 'new_message', data)
    
    # send message back to sender via HTTP response
    data["message"] = render_template("chat/message.html", message=new_message, user_id=sender_id)
    return jsonify(data)

@chat_bp.route('/get_message/<channel_id>')
@login_required
def get_messages(channel_id):
    messages = Message.query.filter_by(channel_id=channel_id).all()

    return jsonify([ render_template("chat/message.html", message=message, user_id=current_user.id) for message in messages])

@chat_bp.route("/pusher/auth", methods=['POST'])
@login_required
def pusher_authentication():
    channel_name = request.form.get('channel_name')
    socket_id = request.form.get('socket_id')

    auth = pusher.authenticate(
        channel=channel_name,
        socket_id=socket_id
    )

    return jsonify(auth)