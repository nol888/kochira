"""
Procedural string generation from predefined formulae.

Creates text by picking n strings from a list of x strings
and concatenating them.
"""

import random
import re

from collections import namedtuple
from functools import partial
from kochira.service import Service

service = Service(__name__, __doc__)

stringify = lambda x: "".join([str(y) for y in x]) if isinstance(x, list) else str(x)
PickFrom = namedtuple("PickFrom", ["num", "list"])
PickFrom.__str__ = lambda self: "".join(stringify(random.choice(self.list)) for _ in range(int(self.num)))
WrapWith = namedtuple("WrapWith", ["times", "wrapper", "body"])
WrapWith.__str__ = lambda self: str(self.wrapper).format(self.body) if int(self.times) <= 1 else str(WrapWith(int(self.times) - 1, self.wrapper, str(self.wrapper).format(self.body)))
RandomInt = namedtuple("RandomInt", ["min", "max"])
RandomInt.__int__ = lambda self: random.randint(self.min, self.max)

def run_generator(*args):
    return "".join(str(x) for x in args)

def bind_generator(name, fn, doc):
    @service.command("pretend you're a {} programmer".format(re.escape(name)), mention=True)
    @service.command(":{}:".format(re.escape(name)))
    def command(ctx):
        ctx.respond(fn())
    command.__doc__ = doc

java = partial(run_generator,
               PickFrom(1, [
                    "",
                    "Abstract",
                    "Basic",
                    "Virtual",
                    "Intermediate",
                    "Advanced",
                    "Composite"
               ]),
               PickFrom(RandomInt(3, 5), [
                    "Request",
                    "Delegate",
                    "Filter",
                    "Chain",
                    "Context",
                    "Proxy",
                    "Handler",
                    "Listener",
                    "Observer",
                    "Visitor",
                    "Client",
                    "Command",
                    "Mediator",
                    "Interpreter",
               ]),
               PickFrom(1, [
                    "",
                    "Impl",
                    "Factory",
                    "Adaptor",
                    "Decorator",
                    "Memento",
                    "Bridge",
                    "Builder",
                    "Singleton",
                    "State",
                    "Strategy",
                    "Multiton",
                    "Prototype",
                    "Controller",
                    "Wrapper",
                    "Facade",
                    "Specification",
                    "Monitor",
                    "Reactor",
                    "Proactor",
               ])
               )

sepples = partial(run_generator,
                  WrapWith(RandomInt(5, 10),
                           PickFrom(1, [
                               "namespace detail {{ {} }}",
                                "template<typename T> class allocator {{ {} }}",
                                "namespace traits {{ {} }}",
                                "const char * foo(const T &t, void(T::*f_t)) const {{ {} }}",
                                "template<typename THead, typename TTail...> class linked_allocator<THead, TTail...> {{ {} }}",
                                "T move(T&& t, U<T>) {{ {} }}"
                           ]),
                           PickFrom(1, [
                               "typedef typename detail::ref<T>::type detail_ref_t;",
                               "return dynamic_cast<T<TTail...>&>(*this);",
                               "detail::replace<T, U>(std::forward<T>(x));"
                           ])
                           )
                  )

python = partial(run_generator,
                 WrapWith(RandomInt(4, 8),
                          PickFrom(1, [
                              "(lambda x: self._(x))({})",
                              "[{} for _ in range(5)]",
                              "reduce(lambda x: self._(x), [{} for _ in range(5)])",
                              "(self.__dict__ for _ in range(5) if {0} == self.garlpy() else _)",
                              "partial(name.replace, {})",
                              "\", \".join({})"
                          ]),
                          PickFrom(1, [
                              "x if self.test() else y",
                              "\" \".join(range(1, 30))",
                              "{'rfw': 'loser', 'Shiz': 'winner'}"
                          ])
                          )
                 )


csharp = partial(run_generator,
               PickFrom(1, [
                    "UI",
                    "SqlFacet",
                    "SqlContext",
                    "COM",
                    "COM",
                    "Native",
                    "Invalid",
                    "Linq",
                    "Xml",
                    "Http",
                    "Buffered",
                    "ByteArray",
                    "AppDomain",
                    "Application",
                    "Context",
                    "TextField",
                    "Activity",
                    "Buffered",
                    "Component",
                    "Collection",
                    "Net"
               ]),
               PickFrom(RandomInt(3, 5), [
                    "Request",
                    "Delegate",
                    "Enumeration",
                    "Prototype",
                    "Runtime",
                    "Transaction",
                    "Thread",
                    "Action",
                    ""
               ]),
               PickFrom(1, [
                    "",
                    "Fallback",
                    "Buffer",
                    "Proxy",
                    "Exception",
                    "Provider",
                    "Listener",
                    "Event",
                    "Handler"
               ]),
               PickFrom(1, [
                "",
                "",
                "",
                "32"
               ])
               )

win32 = partial(run_generator,
                PickFrom(1, [
                    "CHAR ",
                    "DWORD ",
                    "HANDLE ",
                    "HINSTANCE ",
                    "HMODULE ",
                    "HRESULT ",
                    "HWND ",
                    "INT ",
                    "VOID ",
                ]),
                PickFrom(1, [
                    "__stdcall ",
                    "CALLBACK ",
                    "WINAPI ",
                    "",
                    "",
                ]),
                PickFrom(1, [
                    "Co",
                    "Nls",
                    "NtUser",
                    "Reg",
                    "Rtl",
                    "SH",
                    "WSA",
                    "",
                    "",
                ]),
                PickFrom(1, [
                    "Apply",
                    "Create",
                    "Destroy",
                    "Enum",
                    "Find",
                    "Initialize",
                    "Is",
                    "Get",
                    "Handle",
                    "Marshal",
                    "Parse",
                    "Post",
                    "Query",
                    "Receive",
                    "Reset",
                    "Resize",
                    "Run",
                    "Send",
                    "Set",
                    "Unmarshal",
                ]),
                PickFrom(RandomInt(1, 3), [
                    "Buffer",
                    "Console",
                    "Context",
                    "Error",
                    "File",
                    "Format",
                    "Interface",
                    "Id",
                    "Io",
                    "Item",
                    "Language",
                    "Locale",
                    "Media",
                    "Message",
                    "Mode",
                    "Module",
                    "Object",
                    "Operation",
                    "Proc",
                    "Security",
                    "System",
                    "Time",
                    "Window",
                ]),
                PickFrom(1, [
                    "Ex",
                    "2",
                    "64",
                    "",
                    "",
                    "",
                ]),
                WrapWith(1, '({}NULL)',
                    PickFrom(RandomInt(3, 5), [
                        "BOOL bWait, ",
                        "DWORD dwFlags, ",
                        "HANDLE handle, "
                        "HGLOBAL hGlobal, ",
                        "HWND hWnd, ",
                        "LCID locale, ",
                        "LPCTSTR lpName, ",
                        "LPSECURITY_ATTRIBUTES lpAttributes, ",
                        "LPSTREAM lpStream, ",
                        "LPTSTR lpResult, ",
                        "LPVOID lpReserved, ",
                        "LPVOID lpBuffer, ",
                        "PCZZSTR pLocation, ",
                        "SIZE_T dwLength, ",
                        "WPARAM wParam, ",
                        "NULL, ",
                        "NULL, ",
                        "NULL, ",
                    ]),
                ),
                )

bind_generator("c#", csharp,
"""
C# programmer simulator.

Generates a typical C# class name.
""")

bind_generator("java", java,
"""
Java programmer simulator.

Generates a typical Java class name.
""")

bind_generator("c++", sepples,
"""
C++ programmer simulator.

Generates typical C++ code.
""")

bind_generator("python", python,
"""
Python programmer simulator.

Generates typical Python code.
""")

bind_generator("win32", win32,
"""
Win32 API user simulator.

Generates typical Win32 API declarations.
""")
