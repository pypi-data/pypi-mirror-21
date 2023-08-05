

from prompt_toolkit.enums import DEFAULT_BUFFER, SEARCH_BUFFER
from prompt_toolkit.layout.containers import VSplit, HSplit, \
Window, FloatContainer, Float, ConditionalContainer
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.lexers import PygmentsLexer

from prompt_toolkit.filters import Filter, Always, IsDone, HasFocus, RendererHeightIsKnown
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.layout.processors import HighlightSearchProcessor, \
    HighlightSelectionProcessor, \
    ConditionalProcessor, AppendAutoSuggestion
from prompt_toolkit.layout.lexers import Lexer as PromptLex
from prompt_toolkit.layout.prompt import DefaultPrompt
from prompt_toolkit.layout.screen import Char

from pygments.token import Token
from pygments.lexer import Lexer as PygLex

import azclishell.configuration
from azclishell.key_bindings import get_show_default, get_symbols

# from azclishell.az_lexer import ExampleLexer, ToolbarLexer
# from azclishell.az_lexer import ExampleLexer, ToolbarLexer

MAX_COMPLETION = 16
DEFAULT_COMMAND = ""

class HasDefaultScope(Filter):
    def __call__(self, *a, **kw):
        global DEFAULT_COMMAND
        return DEFAULT_COMMAND == ""

# TODO fix this somehow
input_processors = [
    ConditionalProcessor(
        # By default, only highlight search when the search
        # input has the focus. (Note that this doesn't mean
        # there is no search: the Vi 'n' binding for instance
        # still allows to jump to the next match in
        # navigation mode.)
        HighlightSearchProcessor(preview_search=Always()),
        HasFocus(SEARCH_BUFFER)),
    HighlightSelectionProcessor(),
    ConditionalProcessor(
        AppendAutoSuggestion(), HasFocus(DEFAULT_BUFFER) & HasDefaultScope()),
]

class ShowDefault(Filter):
    """ toggle on and off seeing the default """
    def __call__(self, *a, **kw):
        return get_show_default()

class ShowSymbol(Filter):
    """ toggle showing the symbols """
    def __call__(self, *a, **kw):
        return get_symbols()

def default_command():
    return DEFAULT_COMMAND

def set_default_command(com, add=True):
    global DEFAULT_COMMAND
    if add:
        DEFAULT_COMMAND += " " + com
    else:
        DEFAULT_COMMAND = com

def get_prompt_tokens(cli):
    """ returns prompt tokens """
    return [(Token.Az, 'az%s>> '%DEFAULT_COMMAND)]

def get_height(cli):
    """ gets the height of the cli """
    if not cli.is_done:
        return D(min=8)

def get_tutorial_tokens(cli):
    """ tutorial tokens """
    return [(Token.Toolbar, 'In Tutorial Mode: Press [Enter] after typing each part')]

def get_lexers(lex, examLex,toolLex):
    """ gets all the lexer wrappers """
    if not lex:
        return None, None, None
    lexer = None
    if issubclass(lex, PromptLex):
        lexer = lex
    elif issubclass(lex, PygLex):
        lexer = PygmentsLexer(lex)

    if examLex:
        if issubclass(examLex, PygLex):
            examLex = PygmentsLexer(examLex)
    if toolLex:
        if issubclass(toolLex, PygLex):
            toolLex = PygmentsLexer(toolLex)
    return lexer, examLex, toolLex

def create_layout_completions(lex):
    """ layout for example tutorial """
    lexer, _, _ = get_lexers(lex, None, None)
    layout_full = HSplit([
        FloatContainer(
            Window(
                BufferControl(
                    input_processors=input_processors,
                    lexer=lexer,
                    preview_search=Always()),
                get_height=get_height,
            ),
            [
                Float(xcursor=True,
                      ycursor=True,
                      content=CompletionsMenu(
                          max_height=MAX_COMPLETION,
                          scroll_offset=1,
                          extra_filter=(HasFocus(DEFAULT_BUFFER))
                          ))
            ]),
        ConditionalContainer(
            HSplit([
                get_hline(),
                get_param(lexer),
                get_hline(),
                Window(
                    content=BufferControl(
                        buffer_name='example_line',
                        lexer=lexer
                    ),
                ),
                Window(
                    TokenListControl(
                        get_tutorial_tokens,
                        default_char=Char(' ', Token.Toolbar)),
                    height=D.exact(1)),
            ]),
            filter=~IsDone() & RendererHeightIsKnown()
        )
    ])
    return layout_full

def create_layout(lex, examLex, toolbarLex):
    """ creates the layout """
    config = azclishell.configuration.CONFIGURATION
    lexer, examLex, toolbarLex = get_lexers(lex, examLex, toolbarLex)

    input_processors.append(DefaultPrompt(get_prompt_tokens))

    layout_lower = ConditionalContainer(
        HSplit([
            get_anyhline(config),
            get_descriptions(config, examLex, lexer),
            get_examplehline(config),
            get_example(config, examLex),

            ConditionalContainer(
                get_hline(),
                filter=ShowDefault() | ShowSymbol()
            ),
            ConditionalContainer(
                Window(
                    content=BufferControl(
                        buffer_name='default_values',
                        lexer=lexer
                    )
                ),
                filter=ShowDefault()
            ),
            ConditionalContainer(
                get_hline(),
                filter=ShowDefault() & ShowSymbol()
            ),
            ConditionalContainer(
                Window(
                    content=BufferControl(
                        buffer_name='symbols',
                        lexer=examLex
                    )
                ),
                filter=ShowSymbol()
            ),
            Window(
                content=BufferControl(
                    buffer_name='bottom_toolbar',
                    lexer=toolbarLex
                ),
            ),
        ]),
        filter=~IsDone() & RendererHeightIsKnown()
    )

    layout_full = HSplit([
        FloatContainer(
            Window(
                BufferControl(
                    input_processors=input_processors,
                    lexer=lexer,
                    preview_search=Always()),
                get_height=get_height,
            ),
            [
                Float(xcursor=True,
                      ycursor=True,
                      content=CompletionsMenu(
                          max_height=MAX_COMPLETION,
                          scroll_offset=1,
                          extra_filter=(HasFocus(DEFAULT_BUFFER))
                          ))
            ]),
        layout_lower])

    return layout_full


def get_anyhline(config):
    """ if there is a line between descriptions and example """
    if config.BOOLEAN_STATES[config.config.get('Layout', 'command_description')] or\
    config.BOOLEAN_STATES[config.config.get('Layout', 'param_description')]:
        return Window(
            width=D.exact(1),
            height=D.exact(1),
            content=FillControl('-', token=Token.Line))
    else:
        return get_empty()

def get_descript(lexer):
    """ command description window """
    return Window(
        content=BufferControl(
            buffer_name="description",
            lexer=lexer

            ),
        )

def get_param(lexer):
    """ parameter description window """
    return Window(
        content=BufferControl(
            buffer_name="parameter",
            lexer=lexer
            ),
        )

def get_example(config, examLex):
    """ example description window """
    if config.BOOLEAN_STATES[config.config.get('Layout', 'examples')]:
        return Window(
            content=BufferControl(
                buffer_name="examples",
                lexer=examLex
                ),
            )
    else:
        return get_empty()

def get_examplehline(config):
    """ gets a line if there are examples """
    if config.BOOLEAN_STATES[config.config.get('Layout', 'examples')]:
        return get_hline()
    else:
        return get_empty()

def get_empty():
    """ returns an empty window because of syntaxical issues """
    return Window(
        content=FillControl(' ')
    )

def get_hline():
    """ gets a horiztonal line """
    return Window(
        width=D.exact(1),
        height=D.exact(1),
        content=FillControl('-', token=Token.Line))

def get_vline():
    """ gets a vertical line """
    return Window(
        width=D.exact(1),
        height=D.exact(1),
        content=FillControl('*', token=Token.Line))

def get_descriptions(config, examLex, lexer):
    """ based on the configuration settings determines which windows to include """
    if config.BOOLEAN_STATES[config.config.get('Layout', 'command_description')]:
        if config.BOOLEAN_STATES[config.config.get('Layout', 'param_description')]:
            return VSplit([
                get_descript(examLex),
                get_vline(),
                get_param(lexer),
            ])
        else:
            return get_descript(examLex)
    elif config.BOOLEAN_STATES[config.config.get('Layout', 'param_description')]:
        return get_param(lexer)
    else:
        return get_empty()

