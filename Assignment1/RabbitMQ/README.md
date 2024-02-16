# Building a YouTube-like application with RabbitMQ

## Description

We have built a simplified version of a YouTube application using RabbitMQ. The system will consist of three components:
Youtuber , User , YouTubeServer

## Usage

### YoutubeServer.py

Starts the main server. Takes no arguments.

### Youtuber.py

Starts the Youtuber service. Takes youtuber name(must be a single word) and videoname(may be multiple words) respectively as arguments.

### User.py

Starts the User service. Takes username as necessary argument. Other than this, it may have exactly 2 more arguments. These are 's' and 'u' as first argument and Youtuber name as second argument.

## Order of Usage

To use the project, follow the steps below:

1. Start the `YoutubeServer.py` script.
2. Use the `Youtuber.py` script to perform specific actions related to the project.
3. Use the `User.py` script to interact with the project from a user's perspective.

Sample commands:
`python3 YoutubeServer.py`
`python3 Youtuber.py Weeknd Starboy`
`python3 Youtuber.py Alan Alone`
`python3 User.py user1 s Weeknd`
`python3 User.py user1 u Weeknd`
`python3 User.py user2 s Alan`
`python3 Youtuber.py Weeknd After Hours`

## Acknowledgements

Use the official tutorial: https://www.rabbitmq.com/install-windows.html