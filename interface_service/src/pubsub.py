"""Provides a `subscribe` function
   That creats a new subscription to a Pub/Sub topic.
"""

import uuid

from google.auth.credentials import AnonymousCredentials
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

from src.config import settings
from src.var_names import VarNames


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
    pubsub_host = settings[VarNames.PUBSUB_HOST]
    if pubsub_host is None:
        subscriber = pubsub_v1.SubscriberClient()
    else:
        # Connect to configured (emulator) PubSub
        subscriber = pubsub_v1.SubscriberClient(
            client_options={"api_endpoint": pubsub_host},
            credentials=AnonymousCredentials()
        )

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:

        # Get the topic path
        topic_path = subscriber.topic_path(
            settings[VarNames.PUBSUB_PROJECT_ID.value],
            settings[VarNames.PUBSUB_TOPIC_ID.value])

        suffix = "-" + str(uuid.uuid4()) if unique_subscription_name else ''

        # Get the subscriber path
        subscription_path = subscriber.subscription_path(
            settings[VarNames.PUBSUB_PROJECT_ID.value],
            settings[VarNames.PUBSUB_SUBSCRIPTION_ID.value] + suffix)

        # If the subscription name is unique, no need
        # To check if the topic already exists.
        if unique_subscription_name:

            # Create the subscription
            subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )

        else:
            try:

                # Try to create a subscription
                subscriber.create_subscription(
                    request={"name": subscription_path, "topic": topic_path}
                )

            except AlreadyExists:

                # If the subscription already exists, retrieve it
                subscriber.get_subscription(
                    subscription=f'projects/{settings[VarNames.PUBSUB_PROJECT_ID.value]}\
                    /subscriptions/{settings[VarNames.PUBSUB_SUBSCRIPTION_ID.value]}')

        # Subscribe to the topic
        subscriber.subscribe(subscription_path, callback=callback)


if __name__ == '__main__':
    subscribe()
