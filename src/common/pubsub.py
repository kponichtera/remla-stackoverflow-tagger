"""Provides a `subscribe` function
   That creates a new subscription to a Pub/Sub topic.
"""
import os
import uuid
from typing import Callable
from google.api_core.exceptions import NotFound
from common.color_module import ColorsPrinter
from google.cloud.pubsub_v1.subscriber.message import Message
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient


def publish_to_topic(topic_path: str):
    """Creates a publisher to a given topic and creates that topic.

    Args:
        topic_path (str): topic we want to publish to or just create a topic
    """
    publisher = PublisherClient()
    colored_topic_path = ColorsPrinter.get_color_string(
        topic_path,
        ColorsPrinter.OK_BLUE
    )
    #with publisher:
    try:
        # Check if the topic exists
        publisher.get_topic(request={"topic": topic_path})
        ColorsPrinter.log_print_warning(f'Topic {colored_topic_path} exists ⚠️')
    except NotFound:
        # If the topic doesn't exist, create it
        ColorsPrinter.log_print_info(f'Creating topic {colored_topic_path}')
        publisher.create_topic(request={"name": topic_path})
        ColorsPrinter.log_print_info(f'Topic created {colored_topic_path} ✔️')
    return publisher

def subscribe_to_topic(pubsub_host : str, pubsub_project_id : str,
                       pubsub_subscription_id : str, pubsub_subscription_topic_id : str,
                       rec_msg_callback : Callable[[Message], None],
                       unique_subscription_name=False):
    """Subscribes to a Pub/Sub topic.

    Args:
        pubsub_host (str): host of the pubsub queue
        pubsub_project_id (str): project id on pubsub
        pubsub_subscription_id (str): subscription id on pubsub
        pubsub_subscription_topic_id (str): subscription topic id on pubsub
        rec_msg_callback (Callable[[Message], None]): callback on handling messages
                    coming from subscription topic
        unique_subscription_name (bool, optional): Whether to create a unique subscription name.
                This should be enabled for the interface services. Defaults to False.

    Returns:
        (tuple[SubscriberClient, StreamingPullFuture | Unbound]): 
                subscriber client and streaming pull for async operations
    """
    # Create the client
    if pubsub_host is not None:
        colored_host = ColorsPrinter.get_color_string(pubsub_host, ColorsPrinter.OK_BLUE)
        ColorsPrinter.log_print_info(
            f'Using PubSub emulator on host: {colored_host}'
        )
        os.environ["PUBSUB_EMULATOR_HOST"] = pubsub_host

    ColorsPrinter.log_print_info('Connecting to Google Cloud PubSub')
    subscriber = SubscriberClient()

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    # Get the topic path
    topic_path = subscriber.topic_path(
        pubsub_project_id,
        pubsub_subscription_topic_id
    )
    publish_to_topic(topic_path)
    # Suffix needed for unique names
    suffix = ("-" + str(uuid.uuid4())) if unique_subscription_name else ''
    # Get the subscriber path
    subscription_path = subscriber.subscription_path(
        pubsub_project_id,
        pubsub_subscription_id + suffix)
    # If the subscription name is unique, no need
    # To check if the topic already exists.
    colored_subscription_path = ColorsPrinter.get_color_string(
        subscription_path,
        ColorsPrinter.OK_BLUE
    )
    colored_topic_path = ColorsPrinter.get_color_string(
        topic_path,
        ColorsPrinter.OK_BLUE
    )
    if unique_subscription_name:
        # Create the subscription
        ColorsPrinter.log_print_info(
            f'Creating subscription {colored_subscription_path} on topic {colored_topic_path}'
        )
        subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
    else:
        try:
            # Check if the subscription exists
            subscriber.get_subscription(subscription=subscription_path)
            print(f'Subscription {colored_subscription_path} exists ⚠️')
        except NotFound:
            # If it does not exist, create the subscription
            ColorsPrinter.log_print_info(
                f'Creating subscription {colored_subscription_path} on topic {colored_topic_path}'
            )
            subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
    # Subscribe to the topic
    ColorsPrinter.log_print_info(f'Subscribing to subscription {colored_subscription_path}')
    try:
        streaming_pull_future = subscriber.subscribe(
            subscription_path,
            callback=rec_msg_callback
        )
        ColorsPrinter.log_print_info(f'Subscribed to {colored_subscription_path} ✔️')
    except NotFound:
        ColorsPrinter.log_print_fail(f'Failed to subscribe to {colored_subscription_path} ❌')
    return subscriber, streaming_pull_future
