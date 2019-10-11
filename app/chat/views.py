from flask import request, jsonify
from flask_login import login_required, current_user
from app import pusher, db
from app.chat import bp as chat_bp
from app.models import User, Channel, Message


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
        "channel_name": channel.name
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

    new_message = Message(body=message, channel_id=channel)
    new_message.sender_id = sender_id
    new_message.recipient_id = recipient_id
    db.session.add(new_message)
    db.session.commit()

    # send the message to other user
    pusher.trigger(channel, 'new_message', data)

    return jsonify(data)