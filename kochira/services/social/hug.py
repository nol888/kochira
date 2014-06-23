"""
Need a hug?
"""

from kochira.service import Service

service = Service(__name__, __doc__)


@service.setup
def huggables(ctx):
    ctx.storage.huggable = set([])


@service.hook("channel_message")
def need_a_hug(ctx, target, origin, message):
    message = message.strip()

    k = (ctx.client.name, ctx.target)

    if any(t in message for t in [":(", ":-(", ":'(", "QQ", ":C", "T_T",
                                  ";_;", ":c"]):
        ctx.client.ctcp(ctx.channel,
                        "ACTION " + ctx._("hugs {who}").format(who=ctx.origin))
    elif any(t in message.lower() for t in ["hate this", "sad", "i need a hug",
                                            "i'm sad", "fml", "this is crap",
                                            "i need a drink"]):
        ctx.respond("Need a hug?")
        ctx.storage.huggable.add(k)
    elif message.lower() in ["yes", "yup", "yeah", "yep"] and \
        k in ctx.storage.huggable:
        ctx.respond(">--:)--<")
        ctx.storage.huggable.remove(k)
