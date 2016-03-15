"""
Add to a number.

Not actually a game.
"""

from peewee import IntegerField

from kochira.db import Model
from kochira.service import Service

service = Service(__name__, __doc__)


@service.model
class Add(Model):
    number = IntegerField()


DUDE_WEED_LMAO = r"""BLAZE IT

                  |
                 |.|
                 |.|
                |\./|
                |\./|
.               |\./|               .
 \^.\          |\\.//|          /.^/
  \--.|\       |\\.//|       /|.--/
    \--.| \    |\\.//|    / |.--/
     \---.|\    |\./|    /|.---/
        \--.|\  |\./|  /|.--/
           \ .\  |.|  /. /
 _ -_^_^_^_-  \ \\ // /  -_^_^_^_- _
   - -/_/_/- ^_^/| |\^_^ -\_\_\- -
             /_ / | \ _\
                  |
"""


SPOOKY_DEVIL = r"""SPOOKY

                              /       /
                           .'<_.-._.'<
                          /           \      .^.
        ._               |  -+- -+-    |    (_|_)
     r- |\                \   /       /      // 
   /\ \\  :                \  -=-    /       \\
    `. \\.'           ___.__`..;._.-'---...  //
      ``\\      __.--"        `;'     __   `-.  
        /\\.--""      __.,              ""-.  ".
        ;=r    __.---"   | `__    __'   / .'  .'
        '=/\\""           \             .'  .'
            \\             |  __ __    /   |
             \\            |  -- --   //`'`'
              \\           |  -- --  ' | //
               \\          |    .      |// AsH
"""

@service.command("f", mention=False, allow_private=False)
def add(ctx):
    """
    Add to the number.

    Uh, yeah.
    """
    try:
        a = Add.get()
    except Add.DoesNotExist:
        a = Add.create(number=0)
    a.number += 1
    a.save()

    ctx.respond(ctx._("Thanks, the number of respects paid is now {number}.").format(
        number=a.number
    ))

    if a.number == 420:
        for l in DUDE_WEED_LMAO.split("\n"):
            ctx.message("\x02\x033" + l)
    elif a.number == 666:
        for l in SPOOKY_DEVIL.split("\n"):
            ctx.message("\x02\x034" + l)
