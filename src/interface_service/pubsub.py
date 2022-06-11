"""Provides a `subscribe` function
   That creats a new subscription to a Pub/Sub topic.
"""
import os
import uuid

from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound

from config import settings
from var_names import VarNames


def subscribe(unique_subscription_name: bool = False):
    """Subscribes to a Pub/Sub topic.

    Args:
        unique_subscription_name (bool, optional): Whether to create a unique subscription name.
        This should be enabled for the interface services. Defaults to False.
    """

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        """Acknowledges a Pub/Sub message. Used in the `subscribe()` function.

        Args:
            message (pubsub_v1.subscriber.message.Message): The message
            to acknowledge.
        """
        message.ack()

    # Create the client
    pubsub_host = settings[VarNames.PUBSUB_EMULATOR_HOST.value]
    if pubsub_host is not None:
        print('Using PubSub emulator on host:', pubsub_host)
        os.environ["PUBSUB_EMULATOR_HOST"] = pubsub_host

    print('Connecting to Google Cloud PubSub')
    subscriber = pubsub_v1.SubscriberClient()
    publisher = pubsub_v1.PublisherClient()

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:

        # Get the topic path
        topic_path = subscriber.topic_path(
            settings[VarNames.PUBSUB_PROJECT_ID.value],
            settings[VarNames.PUBSUB_TOPIC_ID.value])

        try:
            # Check if the topic exists
            publisher.get_topic(request={"topic": topic_path})
            print(f'Topic {topic_path} exists')
        except NotFound:
            # If the topic doesn't exist, create it
            print(f'Creating topic {topic_path}')
            publisher.create_topic(request={"name": topic_path})

        # Suffix needed for unique names
        suffix = ("-" + str(uuid.uuid4())) if unique_subscription_name else ''

        # Get the subscriber path
        subscription_path = subscriber.subscription_path(
            settings[VarNames.PUBSUB_PROJECT_ID.value],
            settings[VarNames.PUBSUB_SUBSCRIPTION_ID.value] + suffix)

        # If the subscription name is unique, no need
        # To check if the topic already exists.
        if unique_subscription_name:
            # Create the subscription
            print(f'Creating subscription {subscription_path} on topic {topic_path}')
            subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
        else:
            try:
                # Check if the subscription exists
                subscriber.get_subscription(subscription=subscription_path)
                print(f'Subscription {subscription_path} exists')
            except NotFound:
                # If it does not exist, create the subscription
                print(f'Creating subscription {subscription_path} on topic {topic_path}')
                subscriber.create_subscription(
                    request={"name": subscription_path, "topic": topic_path}
                )
        # Subscribe to the topic
        print(f'Subscribing to subscription {subscription_path}')
        subscriber.subscribe(subscription_path, callback=callback)


if __name__ == '__main__':
    subscribe()
