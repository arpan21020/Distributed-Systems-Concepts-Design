import time
import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def updateSubscription(username, action, youtuber):
    # channel.queue_declare(queue='user_requests', durable=True)
    if action=='s':
        subscribe = True  
    else:
        subscribe = False
    request = {
        "user": f"{username}",
        "youtuber": f"{youtuber}",
        "subscribe": f"{subscribe}"
    }
    
    # Sending request message to server
    channel.basic_publish(exchange='',routing_key='user_requests',body=json.dumps(request),properties=pika.BasicProperties(delivery_mode = 2))
    
    print("Subscription Updation Request Successfully Sent. Request Details:")
    print(f"User: {username}")
    print(f"Action: {action}")
    print(f"YouTuber: {youtuber}")

def receiveNotifications(username):
    # print(f"Receiving notifications for {username}")
    # Declare the queue
    # channel.queue_declare(queue='user_notifications', durable=True)
    # send the username for sending notifications for that user
    
    channel.basic_publish(exchange='', routing_key='user_who_get_notifications', body=username, properties=pika.BasicProperties(delivery_mode = 2))
    
    # Receive notifications
    def callback(ch, method, properties, body):
        # print(" [x] Received Notification")
        notification = json.loads(body.decode())
        if (notification == []):
            # print("No new notifications.")
            pass
        # list of strings
        for i in notification:
            print(f"New Notification: {i}")
    time.sleep(1)
    channel.basic_consume(queue=f'{username}_notif', on_message_callback=callback, auto_ack=True)
    print("Waiting for notifications...")
    channel.start_consuming()

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Invalid Command. Usage: python User.py <username> [<action> <youtuber>]")
        sys.exit(1)

    username = sys.argv[1]
    if len(sys.argv) == 2:
        print("Recieving notifications... Press 'Ctrl+C' to stop.")
        try:
            # while True:
            receiveNotifications(username)
        except KeyboardInterrupt:
            print("Stopped receiving notifications.")
    else:
        action = sys.argv[2]
        if action not in ['s', 'u']:
            print("Invalid action. Use 's' for subscribe or 'u' for unsubscribe.")        
        elif len(sys.argv) == 3:
            print("Please provide the YouTuber's name as well.")
        else :
            youtuber = sys.argv[3]
            updateSubscription(username, action, youtuber)
            print("\nRecieving notifications... Press 'Ctrl+C' to stop.")
            try:
                while True:
                    receiveNotifications(username)
                    time.sleep(0.01)
            except KeyboardInterrupt:
                print("Stopped receiving notifications.")

connection.close()
