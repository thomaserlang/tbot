from httpx import AsyncClient

from tbot2.common import ChatMessage
from tbot2.config_settings import config

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars

faceit_client = AsyncClient(
    base_url='https://open.faceit.com/data/v4',
    headers={
        'Authorization': f'Bearer {config.faceit_apikey}',
    },
)


@fills_vars(
    provider='all',
    vars=(
        'faceit.username',
        'faceit.elo',
        'faceit.level',
        'faceit.next_level_points',
        'faceit.next_level',
    ),
)
async def faceit_elo_vars(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    if not vars['faceit.username'].args:
        raise CommandError('{faceit.username <username>} is missing')

    elos = (
        (1, '1'),
        (801, '2'),
        (951, '3'),
        (1101, '4'),
        (1251, '5'),
        (1401, '6'),
        (1551, '7'),
        (1701, '8'),
        (1851, '9'),
        (2001, '10'),
    )

    username = vars['faceit.username'].args[0]
    response = await faceit_client.get('/players', params={'nickname': username})
    if response.status_code == 404:
        raise CommandError(
            f'Unknow user on Faceit "{username}" (usernames are case sensitive)'
        )
    elif response.status_code >= 400:
        raise CommandError(f'Faceit error: {response.text}')
    data = response.json()
    if 'cs2' not in data['games']:
        raise CommandError('The user does not have cs2 in their Faceit profile')

    next_level_points = 0
    next_level = 'unknown'
    for i, e in enumerate(elos):
        if e[0] < data['games']['cs2']['faceit_elo']:
            if i + 1 < len(elos):
                next_level = elos[i + 1][1]
                next_level_points = elos[i + 1][0] - data['games']['cs2']['faceit_elo']

    vars['faceit.username'].value = ''
    vars['faceit.elo'].value = data['games']['cs2']['faceit_elo']
    vars['faceit.level'].value = data['games']['cs2']['skill_level_label']
    vars['faceit.next_level_points'].value = next_level_points
    vars['faceit.next_level'].value = next_level
