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

    # send the message to other user
    pusher.trigger(channelObj.name, 'new_message', data)

    return jsonify(data)

@chat_bp.route('/get_message/<channel_id>')
@login_required
def get_messages(channel_id):
    messages = Message.query.filter_by(channel_id=channel_id).all()

    return jsonify([{
       "id": message.id,
       "message": message.body,
       "sender_id": message.sender_id,
       "recipient_id": message.recipient_id,
       "channel_id": channel_id,
    } for message in messages])