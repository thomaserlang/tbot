from tbot2.channel_quote import (
    ChannelQuoteCreate,
    ChannelQuoteUpdate,
    create_channel_quote,
    delete_channel_quote,
    get_channel_quote_by_number,
    get_random_channel_quote,
    update_channel_quote,
)
from tbot2.common import ChatMessage

from ..exceptions import CommandError, CommandSyntaxError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(provider='all', vars=('quote.add',))
async def quote_add(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    if len(command.args) == 0:
        raise CommandSyntaxError(f'Syntax error, use !{command.name} <your quote>')

    quote = await create_channel_quote(
        channel_id=chat_message.channel_id,
        data=ChannelQuoteCreate(
            message=' '.join(command.args),
            provider=chat_message.provider,
            created_by_provider_viewer_id=chat_message.provider_viewer_id,
            created_by_display_name=chat_message.viewer_display_name,
        ),
    )
    vars['quote.add'].value = f'Quote created with number: {quote.number}'


@fills_vars(provider='all', vars=('quote.edit',))
async def quote_edit(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    if len(command.args) < 2 or not command.args[0].isdigit():
        raise CommandSyntaxError(
            f'Syntax error, use !{command.name} <number> <new text>'
        )

    quote = await get_channel_quote_by_number(
        channel_id=chat_message.channel_id,
        number=int(command.args[0]),
    )
    if not quote:
        raise CommandSyntaxError(f'Unknown quote with number: {command.args[0]}')

    quote = await update_channel_quote(
        quote_id=quote.id,
        data=ChannelQuoteUpdate(
            message=' '.join(command.args[1:]),
        ),
    )
    vars['quote.edit'].value = f'Quote updated with number: {quote.number}'


@fills_vars(provider='all', vars=('quote.delete',))
async def quote_delete(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    if len(command.args) != 1 or not command.args[0].isdigit():
        raise CommandSyntaxError(f'Syntax error, use !{command.name} <number>')

    quote = await get_channel_quote_by_number(
        channel_id=chat_message.channel_id,
        number=int(command.args[0]),
    )
    if not quote:
        raise CommandError(f'Unknown quote with number: {command.args[0]}')

    await delete_channel_quote(
        quote_id=quote.id,
    )
    vars['quote.delete'].value = f'Quote deleted with number: {quote.number}'


@fills_vars(
    provider='all',
    vars=(
        'quote.message',
        'quote.number',
        'quote.user',
        'quote.date',
        'quote.provider',
    ),
)
async def quote_get(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    if len(command.args) > 0:
        if not command.args[0].isdigit():
            raise CommandSyntaxError(f'Syntax error, use !{command.name} <number>')

        quote = await get_channel_quote_by_number(
            channel_id=chat_message.channel_id,
            number=int(command.args[0]),
        )
        if not quote:
            raise CommandError(f'Unknown quote with number: {command.args[0]}')
    else:
        quote = await get_random_channel_quote(
            channel_id=chat_message.channel_id,
        )
        if not quote:
            raise CommandError('No quotes available')

    vars['quote.message'].value = quote.message
    vars['quote.number'].value = str(quote.number)
    vars['quote.user'].value = quote.created_by_display_name
    vars['quote.date'].value = str(quote.created_at)[:10]
    vars['quote.provider'].value = quote.provider
