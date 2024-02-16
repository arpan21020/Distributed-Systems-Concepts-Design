import uuid
import time
import pika
import json
import threading

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# stores the subscriptions of each user; keys are usernames and values are sets of subscribed YouTuber names.
user_subscriptions = {}

# stores notifications for each user; keys are usernames and values are lists of notification messages.
user_notifications = {}

# stores the yt and his videos
videos = {}
# thread3=0
channel.queue_declare(queue='user_requests', durable=True) # sub or unsub
channel.queue_declare(queue='youtuber_requests', durable=True) # video upload
channel.queue_declare(queue='user_who_get_notifications', durable=True) # user who get notifications
users=[]
def consume_user_requests():
    while 1:
        time.sleep(0.1)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            def callback(ch, method, properties, body):
                request = json.loads(body.decode())
                username = request.get('user')
                youtuber = request.get('youtuber')
                subscribe = request.get('subscribe')
                if (username not in users):
                    users.append(username)
                    channel.queue_declare(queue=f'{username}_notif', durable=True) # notifications for user
                # Update user's subscription list and handled the case when the user is not in the user_subscriptions using try-except
                if (user_subscriptions.get(username) == None):
                    user_subscriptions[username] = set()
                if subscribe == "True":
                    # user_subscriptions[username].add(youtuber)
                    try:
                        check = videos[youtuber]
                        # if this gets an error, there is no youtuber named youtuber
                        user_subscriptions[username].add(youtuber)
                        print(f"User {username} has subscribed to {youtuber}")
                    except:
                        print(f"ERROR: Youtuber {youtuber} not found.")
                else:
                    if (youtuber in user_subscriptions[username]):
                        user_subscriptions[username].discard(youtuber)
                        print(f"{username} unsubscribed to {youtuber}")
                    else:
                        # print("subscribe =", subscribe)
                        print(f"ERROR: {username} is not subscribed to {youtuber}")
                    
                
                # # Handle subscription/unsubscription request
                # elif request.get('action') in ['subscribe', 'unsubscribe']:
                #     youtuber_name = request.get('youtuber')
                #     action = "subscribed" if request.get('action') == 'subscribe' else "unsubscribed"
                    
                #     if action == 'subscribed':
                #         try:
                #             user_subscriptions[username].add(youtuber_name)
                #         except KeyError:
                #             user_subscriptions[username] = {youtuber_name}
                #         print(f"{username} {action} to {youtuber_name}")
                #     else:
                #         try:
                #             user_subscriptions[username].discard(youtuber_name)
                #             print(f"{username} {action} to {youtuber_name}")
                #         except KeyError:
                #             print(f"ERROR: {username} is not found. Adding it to the database")
                #             user_subscriptions[username] = set()
                #         except ValueError:
                #             print(f"ERROR: {username} is not subscribed to {youtuber_name}")
                
                print("SUCCESS: Subscription request handled")
                # ch.basic_ack(delivery_tag=method.delivery_tag)
            
            # def callback2(ch, method, properties, body):
            #     username = body
            #     # Send notifications to the user
            #     if username in user_notifications:
            #         # for notification in user_notifications[username]:
            #         channel.basic_publish(exchange='', routing_key='user_notifications', body=json.dumps(user_notifications[username]),properties=pika.BasicProperties(delivery_mode = 2))
            #         # sent the json of list of strings as body
            #         user_notifications[username] = []
            #     else:
            #         channel.basic_publish(exchange='', routing_key='user_notifications', body=json.dumps([]),properties=pika.BasicProperties(delivery_mode = 2))
            #     print(f"Notifications sent to {username}")
            #     ch.basic_ack(delivery_tag=method.delivery_tag)
            c_tag = str(uuid.uuid4())
            channel.basic_consume(queue='user_requests', on_message_callback=callback, auto_ack=True,consumer_tag = c_tag)
            # channel.basic_consume(queue='user_who_get_notifications', on_message_callback=callback2, auto_ack=True)
            # print("Waiting for user requests...")
            # channel.start_consuming()
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                print("Server stopped after receiving interrupt signal")
                exit(1)
        except pika.exceptions.AMQPConnectionError:
            continue
        # except KeyboardInterrupt:
        #     connection.close()
        #     print("Server stopped after receiving interrupt signal")

def consume_youtuber_requests():
    while 1:
        time.sleep(0.1)
        try:    
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            def callback(ch, method, properties, body):
                request = json.loads(body.decode())
                YouTuberName = request.get('YouTuberName')
                videoName = request.get('videoName')
                # add video to the list of videos of the youtubers
                if (videos.get(YouTuberName) != None):
                    videos[YouTuberName].append(videoName)
                else:
                    videos[YouTuberName] = [videoName]
                
                # Notify users subscribed to this YouTuber
                for username, subscriptions in user_subscriptions.items():
                    if YouTuberName in subscriptions:
                        if username not in user_notifications:
                            user_notifications[username] = []
                        user_notifications[username].append(f"{YouTuberName} uploaded {videoName}")
                # notify_users(YouTuberName)
                # thread3.start()
                print(f"SUCCESS: Video '{videoName}' received by the YouTube server. Notifications sent to the users.")
                # send notifications to the users
                for username, subscriptions in user_subscriptions.items():
                    if YouTuberName in subscriptions:
                        channel.basic_publish(exchange='', routing_key='user_who_get_notifications', body=username, properties=pika.BasicProperties(delivery_mode = 2))
    
            c_tag = str(uuid.uuid4())
            channel.basic_consume(queue='youtuber_requests', on_message_callback=callback, auto_ack=True,consumer_tag = c_tag)
            # print("Starting to consume YouTuber requests...")
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                print("Server stopped after receiving interrupt signal")
                exit(1)
        except pika.exceptions.AMQPConnectionError:
            continue
        # except KeyboardInterrupt:
        #     connection.close()
        #     print("Server stopped after receiving interrupt signal")

def notify_users():
    # while 1:
    #     time.sleep(0.1)
    #     try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            # channel.queue_declare(queue='user_notifications', durable=True) # notifications for user
            
            # keep on emptying the user_notifications dictionary and sending the notifications to the users
            def callback(ch, method, properties, body):
                username = body.decode('utf-8')
                # print(username, "is the username!!")
                if (username not in users):
                    users.append(username)
                    channel.queue_declare(queue=f'{username}_notif', durable=True) # notifications for user
                if username in user_notifications.keys():
                    # for notification in user_notifications[username]:
                    channel.basic_publish(exchange='', routing_key=f'{username}_notif', body=json.dumps(user_notifications[username]),properties=pika.BasicProperties(delivery_mode = 2))
                    # sent the json of list of strings as body
                    user_notifications[username] = []
                else:
                    channel.basic_publish(exchange='', routing_key=f'{username}_notif', body=json.dumps([]),properties=pika.BasicProperties(delivery_mode = 2))
                # print(f"Notifications sent to {username}")
                # print("Yes the username is", username)
                # ch.basic_ack(delivery_tag=method.delivery_tag)
            # for username, notifications in user_notifications.items():
            #     channel.basic_publish(exchange='', routing_key='user_notifications', body=json.dumps(notifications), properties=pika.BasicProperties(delivery_mode = 2))
            #     user_notifications[username] = []
            c_tag = str(uuid.uuid4())
            channel.basic_consume(queue='user_who_get_notifications', on_message_callback=callback, auto_ack=True,consumer_tag = c_tag)
            # print("Waiting for user requests...")
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                # connection.close()
                return 1
                # print("Server stopped after receiving interrupt signal")
                # exit(1)
            # channel.start_consuming()
        # except pika.exceptions.AMQPConnectionError:
        #     continue
                
                
        # except KeyboardInterrupt:
        #     connection.close()
        #     print("Server stopped after receiving interrupt signal")
        #     exit(1)
# def start_server():
#     # Make 3 threads and call these functions separately in each of them
    
#     consume_user_requests()
#     consume_youtuber_requests()
#     notify_users()

# start_server()
    
# print a starting message for the server

# def thread_user():
#     consume_user_requests()

# def thread_yt():
#     consume_youtuber_requests()

# def notify_users_forever():
    # while 1:
    #     notify_users()
    #     time.sleep(0.1)


def main():
    print("Started the YouTube server... ")
    # try:
        # # Create threads
    thread1 = threading.Thread(target=consume_user_requests,daemon=True)
    thread2 = threading.Thread(target=consume_youtuber_requests,daemon=True)
    # thread3 = threading.Thread(target=notify_users,daemon=True)
    # thread3 = threading.Thread(target=notify_users_forever)
    # # Start threads
    thread1.start()
    thread2.start()
    t = notify_users()
    # thread3.start()
    if t==1:
        connection.close()
        print("Server stopped after receiving interrupt signal")
        return 

    # # Wait for all threads to complete
    thread1.join()
    thread2.join()
    # thread3.join()
    # consume_user_requests()
    # consume_youtuber_requests()
    # notify_users_forever()

# except KeyboardInterrupt:
#     connection.close()
#     print("Server stopped after receiving interrupt signal")

try:
    main()
except:
    # connection.close()
    print("Server stopped after receiving interrupt signal")
    exit(1)