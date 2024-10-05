from firebase_admin import messaging

def send_push_notification(token, title, body):
    """
    Sends a push notification to a specific device.

    Args:
        token (str): The device token to which the notification is sent.
        title (str): Title of the notification.
        body (str): Body of the notification.
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    try:
        # Send a message to the device corresponding to the provided registration token
        response = messaging.send(message)
        print('Successfully sent message:', response)
        return response
    except Exception as e:
        print(f"Error sending push notification: {e}")
        return None
