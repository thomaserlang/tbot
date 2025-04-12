from tbot2.common import check_pattern_match
from tbot2.common.utils.text_utils import (
    collaps_message_letter_repeat,
    normalize_leetspeak_message,
)
from tbot2.testbase import run_file


def test_check_pattern_match():
    assert check_pattern_match(
        message='test123',
        pattern='test123',
        normalize=True,
        strip_symbols=True,
        collaps_letters=True,
        check_leetspeak=True,
    )
    assert check_pattern_match(
        message='1337 something',
        pattern='leet',
        normalize=True,
        strip_symbols=True,
        collaps_letters=True,
        check_leetspeak=True,
    )
    assert check_pattern_match(message='hello world', pattern='hello world')
    assert check_pattern_match(
        message='hellö world', pattern='hello world', normalize=True
    )
    assert check_pattern_match(
        message='hellø world', pattern='hello world', normalize=True
    )
    assert not check_pattern_match(
        message='hellø world', pattern='hello world', normalize=False
    )
    assert check_pattern_match(message='hello world', pattern='re:[a-z ]+')

    assert check_pattern_match(message='hello world', pattern='"hello world"')
    assert not check_pattern_match(message='world hello', pattern='"hello world"')

    assert check_pattern_match(
        message='this is a test with a hello world that should match',
        pattern='"hello world"',
    )
    assert check_pattern_match(
        message='hello this is a test with a hello world that should match',
        pattern='"hello world"',
    )
    assert check_pattern_match(
        message='hello this is a test with a hello world that should match',
        pattern='"a hello world"',
    )
    assert check_pattern_match(
        message='hello this is a test with a hello! world that should match',
        pattern='"a hello world"',
        strip_symbols=True,
    )
    assert check_pattern_match(
        message='hello this is a test with a hello world that should match',
        pattern='this "hello world"',
    )

    assert not check_pattern_match(
        message='hello this is a test with a hello world that should match',
        pattern='"this hello world"',
    )


def test_collaps_message_letter_repeat():
    assert collaps_message_letter_repeat('helllo') == 'hello'
    assert collaps_message_letter_repeat('helllo world') == 'hello world'
    assert (
        collaps_message_letter_repeat(normalize_leetspeak_message('hello wo000ooorld'))
        == 'hello woorld'
    )


if __name__ == '__main__':
    run_file(__file__)
