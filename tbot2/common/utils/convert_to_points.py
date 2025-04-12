from tbot2.exceptions import ErrorMessage


def convert_to_points(points_str: str | int, user_points: int) -> int:
    if isinstance(points_str, str):
        if points_str.isdigit():
            points_str = int(points_str)
        elif points_str.lower() in ['all', 'allin', 'all-in']:
            points_str = user_points
        elif points_str.lower() == 'half':
            points_str = user_points // 2
        elif points_str.endswith('%'):
            try:
                points_str = int(points_str[:-1]) * user_points // 100
            except ValueError as e:
                raise ErrorMessage(f'Invalid points: {points_str}') from e
        else:
            raise ErrorMessage(f'Invalid points: {points_str}')
    return int(points_str)
