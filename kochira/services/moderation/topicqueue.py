"""
Topic queuing.

Enables users to add text to the topic via a queue of items.
"""

from kochira import config
from kochira.auth import requires_permission
from kochira.service import Service, Config


service = Service(__name__, __doc__)

@service.config
class Config(Config):
    topic_separator = config.Field(doc="Separator to use between topic items.", default=" | ")
    chanserv_topic = config.Field(doc="Ask ChanServ to set the topic.", default=False)


@service.command("add (?P<topic>.+) to topic", mention=True)
@service.command("!topic (?P<topic>.+)")
@requires_permission("topic")
def topic(ctx, topic):
    """
    Prepend to topic.

    Prepends some new text to the topic. If the topic is too long, it will
    evict the oldest part of the topic.
    """

    parts = ctx.client.channels[ctx.target].topic

    if parts:
        parts = parts.split(ctx.config.topic_separator)
    else:
        parts = []

    parts.insert(0, topic)

    while len(ctx.config.topic_separator.join(parts).encode("utf-8")) > ctx.client._topic_length_limit:
        parts.pop()

    message = ctx.config.topic_separator.join(parts)

    if not ctx.config.chanserv_topic:
        ctx.client.set_topic(ctx.target, message)
    else:
        ctx.client.message("ChanServ", "TOPIC {target} {message}".format(target=ctx.target,
                                                                         message=message))
