import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('35.223.43.223'))
channel = connection.channel()

def publishVideo(youtuber, videoName):
    # channel.queue_declare(queue='youtuber_requests', durable=True)
    message = {
        "YouTuberName": youtuber,
        "videoName": videoName
    }
    message_json = json.dumps(message)
    channel.basic_publish(exchange='', routing_key='youtuber_requests', body=message_json,properties=pika.BasicProperties(delivery_mode = 2))

    print("Video succesfully published to YouTube server. Request details: ")
    print(f"YouTuber: {youtuber}")
    print(f"Video: {videoName}")

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Usage: python Youtuber.py <YouTuberName> <videoName>")
        sys.exit(1)

    YouTuberName = sys.argv[1]
    videoName = " ".join(sys.argv[2:])

    # Publish the video
    publishVideo(YouTuberName, videoName)

connection.close()
