def parse_bet_to_int(bet: str | int, user_points: int):
    if isinstance(bet, str):
        if bet.isdigit():
            bet = int(bet)
        elif bet.lower() in ['all', 'allin', 'all-in']:
            bet = user_points
        elif bet.lower() == 'half':
            bet = user_points // 2
        elif bet.endswith('%'):
            try:
                bet = int(bet[:-1]) * user_points // 100
            except ValueError:
                raise ValueError(f'Invalid bet: {bet}')
        else:
            raise ValueError(f'Invalid bet: {bet}')
    return int(bet)
