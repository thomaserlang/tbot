import asyncio
import random
from uuid import UUID

from uuid6 import uuid7

from tbot2.common import (
    ChatMessageBadgeRequest,
    ChatMessageCreate,
    ChatMessagePartRequest,
    EmotePartRequest,
    GiftPartRequest,
    Provider,
)

from ..actions.chat_message_actions import create_chat_message


async def seed_chat_messages(
    *, channel_id: UUID, num_messages: int = 15, wait_after_message: float = 0.1
) -> None:
    if num_messages <= 0:
        return
    usernames: list[tuple[str, str]] = [
        ('viewer1', 'Viewer One'),
        ('gamer123', 'GamerPro123'),
        ('chatfan', 'ChatFan'),
        ('streamer_friend', 'StreamerFriend'),
        ('new_user', 'NewUser'),
        ('loyal_sub', 'LoyalSubscriber'),
        ('random_chatter', 'RandomChatter'),
        ('excited_fan', 'ExcitedFan'),
        ('lurker42', 'Lurker42'),
        ('emoji_lover', 'EmojiLover😊'),
        ('pro_player', 'ProPlayer'),
        ('mod_jane', 'ModJane'),
        ('superfan99', 'SuperFan99'),
        ('silent_watcher', 'SilentWatcher'),
        ('emote_master', 'EmoteMaster'),
        ('hype_train', 'HypeTrain'),
        ('tech_guru', 'TechGuru'),
        ('music_lover', 'MusicLover'),
        ('quizmaster', 'QuizMaster'),
        ('retro_gamer', 'RetroGamer'),
        ('speedrunner', 'SpeedRunner'),
        ('casual_viewer', 'CasualViewer'),
        ('vip_alex', 'VIPAlex'),
        ('meme_lord', 'MemeLord'),
        ('tiktok_star', 'TikTokStar'),
        ('yt_commenter', 'YTCommenter'),
        ('twitch_fan', 'TwitchFan'),
        ('yt_gamer', 'YTGamer'),
        ('ttk_viewer', 'TTKViewer'),
        ('alpha_wolf', 'AlphaWolf'),
        ('beta_tester', 'BetaTester'),
        ('pixel_pirate', 'PixelPirate'),
        ('stream_queen', 'StreamQueen'),
        ('king_kappa', 'KingKappa'),
        ('emote_spammer', 'EmoteSpammer'),
        ('clipper', 'Clipper'),
        ('mod_mike', 'ModMike'),
        ('vip_sam', 'VIPSamantha'),
        ('retro_andy', 'RetroAndy'),
        ('quiz_wiz', 'QuizWiz'),
        ('snack_attack', 'SnackAttack'),
        ('late_night_owl', 'LateNightOwl'),
        ('early_bird', 'EarlyBird'),
        ('hype_beast', 'HypeBeast'),
        ('silent_shadow', 'SilentShadow'),
        ('cosplay_hero', 'CosplayHero'),
        ('anime_fan', 'AnimeFan'),
        ('sports_buff', 'SportsBuff'),
        ('coding_ninja', 'CodingNinja'),
        ('music_maniac', 'MusicManiac'),
        ('pet_lover', 'PetLover'),
        ('travel_bug', 'TravelBug'),
        ('foodie', 'Foodie'),
        ('gadget_guru', 'GadgetGuru'),
        ('movie_buff', 'MovieBuff'),
        ('bookworm', 'Bookworm'),
        ('challenge_ace', 'ChallengeAce'),
        ('fan_artist', 'FanArtist'),
        ('setup_master', 'SetupMaster'),
        ('holiday_hype', 'HolidayHype'),
        ('behind_scenes', 'BehindScenes'),
        ('app_addict', 'AppAddict'),
        ('color_craze', 'ColorCraze'),
        ('animal_friend', 'AnimalFriend'),
        ('cooking_star', 'CookingStar'),
        ('sporty_spirit', 'SportySpirit'),
        ('giveaway_guru', 'GiveawayGuru'),
        ('quote_king', 'QuoteKing'),
        ('sub_star', 'SubStar'),
        ('drink_enthusiast', 'DrinkEnthusiast'),
        ('stream_runner', 'StreamRunner'),
        ('holiday_hero', 'HolidayHero'),
        ('tour_guide', 'TourGuide'),
        ('challenge_champ', 'ChallengeChamp'),
        ('moment_maker', 'MomentMaker'),
        ('reaction_queen', 'ReactionQueen'),
        ('console_collector', 'ConsoleCollector'),
        ('setup_show', 'SetupShow'),
        ('songbird', 'SongBird'),
        ('dance_star', 'DanceStar'),
        ('food_fanatic', 'FoodFanatic'),
        ('horror_gamer', 'HorrorGamer'),
        ('movie_maniac', 'MovieManiac'),
        ('collab_creator', 'CollabCreator'),
        ('color_lover', 'ColorLover'),
        ('retro_fan', 'RetroFan'),
        ('animal_enthusiast', 'AnimalEnthusiast'),
        ('cook_master', 'CookMaster'),
        ('sport_fan', 'SportFan'),
        ('giveaway_star', 'GiveawayStar'),
        ('quote_queen', 'QuoteQueen'),
        ('sub_supporter', 'SubSupporter'),
        ('drink_master', 'DrinkMaster'),
        ('stream_marathon', 'StreamMarathon'),
        ('holiday_fan', 'HolidayFan'),
        ('bts_buff', 'BTSBuff'),
        ('book_buddy', 'BookBuddy'),
        ('tour_star', 'TourStar'),
        ('app_fan', 'AppFan'),
        ('challenge_fan', 'ChallengeFan'),
        ('moment_fan', 'MomentFan'),
        ('fanart_fan', 'FanArtFan'),
    ]

    messages: list[list[ChatMessagePartRequest]] = [
        [ChatMessagePartRequest(type='text', text='Hello everyone!')],
        [ChatMessagePartRequest(type='text', text='How is the stream today?')],
        [ChatMessagePartRequest(type='text', text='LOL that was funny')],
        [ChatMessagePartRequest(type='text', text='Great play!')],
        [ChatMessagePartRequest(type='text', text='I love this game')],
        [
            ChatMessagePartRequest(
                type='text', text='First time watching, this is awesome'
            )
        ],
        [
            ChatMessagePartRequest(
                type='text', text='Can you explain what just happened?'
            )
        ],
        [ChatMessagePartRequest(type='text', text='Followed! Great content')],
        [ChatMessagePartRequest(type='text', text='Where are you from?')],
        [ChatMessagePartRequest(type='text', text='GG')],
        [ChatMessagePartRequest(type='text', text='PogChamp')],
        [ChatMessagePartRequest(type='text', text='How long have you been streaming?')],
        [ChatMessagePartRequest(type='text', text='Any tips for beginners?')],
        [ChatMessagePartRequest(type='text', text='This music is great')],
        [ChatMessagePartRequest(type='text', text='What settings do you use?')],
        [ChatMessagePartRequest(type='text', text="Let's go!")],
        [ChatMessagePartRequest(type='text', text='That was epic!')],
        [ChatMessagePartRequest(type='text', text='Can you do a shoutout?')],
        [ChatMessagePartRequest(type='text', text='Sub hype!')],
        [ChatMessagePartRequest(type='text', text='Who else is watching from mobile?')],
        [ChatMessagePartRequest(type='text', text='I just joined, what did I miss?')],
        [ChatMessagePartRequest(type='text', text='This chat is wild!')],
        [ChatMessagePartRequest(type='text', text='Love the energy here!')],
        [ChatMessagePartRequest(type='text', text='Can you play my favorite song?')],
        [ChatMessagePartRequest(type='text', text='When is the next stream?')],
        [ChatMessagePartRequest(type='text', text='This is trending on TikTok!')],
        [ChatMessagePartRequest(type='text', text='Saw this on YouTube Shorts!')],
        [ChatMessagePartRequest(type='text', text='Twitch chat is the best!')],
        [ChatMessagePartRequest(type='text', text='Anyone else from TikTok?')],
        [ChatMessagePartRequest(type='text', text='YT gang here!')],
        [ChatMessagePartRequest(type='text', text="Let's get some hype in the chat!")],
        [ChatMessagePartRequest(type='text', text='Streamer deserves more viewers!')],
        [ChatMessagePartRequest(type='text', text='What platform do you prefer?')],
        [ChatMessagePartRequest(type='text', text='This is my favorite channel!')],
        [ChatMessagePartRequest(type='text', text='Can you react to this meme?')],
        [ChatMessagePartRequest(type='text', text='Who else is grinding tonight?')],
        [ChatMessagePartRequest(type='text', text="Let's raid someone after!")],
        [ChatMessagePartRequest(type='text', text='I clipped that moment!')],
        [ChatMessagePartRequest(type='text', text='This is so wholesome!')],
        [ChatMessagePartRequest(type='text', text='Can you say hi to me?')],
        [ChatMessagePartRequest(type='text', text="I'm here every stream!")],
        [ChatMessagePartRequest(type='text', text='Can you play another game?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite snack?')],
        [ChatMessagePartRequest(type='text', text='The graphics look amazing!')],
        [ChatMessagePartRequest(type='text', text='Who else is watching from Europe?')],
        [ChatMessagePartRequest(type='text', text='Can you do a giveaway?')],
        [ChatMessagePartRequest(type='text', text='I love your setup!')],
        [ChatMessagePartRequest(type='text', text='What mic are you using?')],
        [ChatMessagePartRequest(type='text', text='This is so relaxing.')],
        [ChatMessagePartRequest(type='text', text='Can you show your pet?')],
        [ChatMessagePartRequest(type='text', text='What time zone are you in?')],
        [ChatMessagePartRequest(type='text', text='I just subscribed!')],
        [ChatMessagePartRequest(type='text', text='Can you do a Q&A?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite streamer?')],
        [ChatMessagePartRequest(type='text', text='This chat is so friendly!')],
        [ChatMessagePartRequest(type='text', text='Can you do a challenge run?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite emote?')],
        [ChatMessagePartRequest(type='text', text='How do you stay so positive?')],
        [ChatMessagePartRequest(type='text', text='Can you play with viewers?')],
        [ChatMessagePartRequest(type='text', text='What is your stream schedule?')],
        [ChatMessagePartRequest(type='text', text='This is the best part!')],
        [ChatMessagePartRequest(type='text', text='Can you speak another language?')],
        [
            ChatMessagePartRequest(
                type='text', text='What is your favorite moment on stream?'
            )
        ],
        [ChatMessagePartRequest(type='text', text='Can you do a speedrun?')],
        [ChatMessagePartRequest(type='text', text='Who else is here every day?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite meme?')],
        [ChatMessagePartRequest(type='text', text='Can you do a reaction stream?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite console?')],
        [ChatMessagePartRequest(type='text', text='Can you show your setup?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite song?')],
        [ChatMessagePartRequest(type='text', text='Can you do a dance?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite food?')],
        [ChatMessagePartRequest(type='text', text='Can you play horror games?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite movie?')],
        [ChatMessagePartRequest(type='text', text='Can you do a collab?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite color?')],
        [ChatMessagePartRequest(type='text', text='Can you play retro games?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite animal?')],
        [ChatMessagePartRequest(type='text', text='Can you do a cooking stream?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite sport?')],
        [ChatMessagePartRequest(type='text', text='Can you do a giveaway soon?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite quote?')],
        [ChatMessagePartRequest(type='text', text='Can you play with subs?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite drink?')],
        [ChatMessagePartRequest(type='text', text='Can you do a 24-hour stream?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite holiday?')],
        [ChatMessagePartRequest(type='text', text='Can you do a behind-the-scenes?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite book?')],
        [ChatMessagePartRequest(type='text', text='Can you do a setup tour?')],
        [ChatMessagePartRequest(type='text', text='What is your favorite app?')],
        [ChatMessagePartRequest(type='text', text='Can you do a challenge?')],
        [
            ChatMessagePartRequest(
                type='text', text='What is your favorite streamer moment?'
            )
        ],
        [ChatMessagePartRequest(type='text', text='Can you do a reaction to fan art?')],
    ]

    emotes: list[ChatMessagePartRequest] = [
        ChatMessagePartRequest(
            type='emote',
            text='pepJAM',
            emote=EmotePartRequest(
                id='01EZY967K0000CYST6006V20T8',
                name='pepJAM',
                animated=True,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='YEP',
            emote=EmotePartRequest(
                id='01F6PPENA80002RDNAW6F35V4X',
                name='YEP',
                animated=True,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='HACKERMANS',
            emote=EmotePartRequest(
                id='01F6WP22CR0004YCK11WAVZHEW',
                name='HACKERMANS',
                animated=True,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='pepeD',
            emote=EmotePartRequest(
                id='01F2ZWD6CR000DSBG200DM9SGM',
                name='pepeD',
                animated=True,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='D:',
            emote=EmotePartRequest(
                id='01GM78BAGR0001WBT5AMQY9YG3',
                name='D:',
                animated=False,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='monkaW',
            emote=EmotePartRequest(
                id='01F6NPHCN0000BEKN8ZXWQNSDC',
                name='monkaW',
                animated=False,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='FeelsRainMan',
            emote=EmotePartRequest(
                id='01EZPGBXMR0001DCZS00AD662R',
                name='FeelsRainMan',
                animated=False,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='MLADY',
            emote=EmotePartRequest(
                id='01F6PYVPP80005CV1Y3Z4X4V4K',
                name='MLADY',
                animated=False,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='monkaS',
            emote=EmotePartRequest(
                id='01F78CHJ2G0005TDSTZFBDGMK4',
                name='monkaS',
                animated=False,
                emote_provider='7tv',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='DansGame',
            emote=EmotePartRequest(
                id='33',
                name='DansGame',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='bahLove',
            emote=EmotePartRequest(
                id='305493055',
                name='bahLove',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='bahHappy',
            emote=EmotePartRequest(
                id='873540',
                name='bahHappy',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='bahTea',
            emote=EmotePartRequest(
                id='302968292',
                name='bahTea',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePartRequest(
            type='emote',
            text='bahLurk',
            emote=EmotePartRequest(
                id='emotesv2_340449fe563e4ee49eba8789a44cb7db',
                name='bahLurk',
                animated=True,
                emote_provider='twitch',
            ),
        ),
    ]

    badges: list[ChatMessageBadgeRequest] = [
        ChatMessageBadgeRequest(
            id='partner-1',
            type='partner-1',
            name='partner-1',
        ),
        ChatMessageBadgeRequest(
            id='founder-0',
            type='founder',
            name='founder',
        ),
        ChatMessageBadgeRequest(
            id='sub-gifter-1000',
            type='sub-gifter-1000',
            name='sub-gifter-1000',
        ),
        ChatMessageBadgeRequest(
            id='rplace-2023-1',
            type='rplace-2023-1',
            name='rplace-2023-1',
        ),
        ChatMessageBadgeRequest(
            id='twitch-recap-2024-1',
            type='twitch-recap-2024-1',
            name='twitch-recap-2024-1',
        ),
        ChatMessageBadgeRequest(
            id='subtember-2024-1',
            type='subtember-2024-1',
            name='subtember-2024-1',
        ),
        ChatMessageBadgeRequest(
            id='gone-bananas-1',
            type='gone-bananas-1',
            name='gone-bananas-1',
        ),
    ]

    providers: list[Provider] = ['twitch', 'youtube', 'tiktok']

    for _ in range(num_messages):
        username, display_name = random.choice(usernames)
        provider_channel_id = str(random.randint(10000, 99999))
        message_parts: list[ChatMessagePartRequest] = [*random.choice(messages)]
        provider = random.choice(providers)
        selected_badges: list[ChatMessageBadgeRequest] = []

        if random.random() < 0.5:
            num_emotes = random.randint(1, 2)
            chosen_emotes = random.sample(emotes, k=num_emotes)
            insert_at = random.randint(0, len(message_parts))
            for emote in chosen_emotes:
                message_parts = (
                    message_parts[:insert_at]
                    + [
                        ChatMessagePartRequest(type='text', text=' '),
                        emote,
                        ChatMessagePartRequest(type='text', text=' '),
                    ]
                    + message_parts[insert_at:]
                )
                insert_at += 2

        if provider == 'twitch':
            if random.random() < 0.0:
                num_badges = random.randint(1, min(3, len(badges)))
                selected_badges = random.sample(badges, k=num_badges)

            if random.random() < 0.05:
                message_parts.extend(
                    [
                        ChatMessagePartRequest(text=' ', type='text'),
                        ChatMessagePartRequest(
                            text='cheer10000',
                            type='gift',
                            gift=GiftPartRequest(
                                id='cheer-10000',
                                name='cheer-10000',
                                type='cheermote',
                                count=10000,
                                animated=True,
                            ),
                        ),
                        ChatMessagePartRequest(text=' ', type='text'),
                        ChatMessagePartRequest(
                            text='cheer1000',
                            type='gift',
                            gift=GiftPartRequest(
                                id='cheer-1000',
                                name='cheer-1000',
                                type='cheermote',
                                count=1000,
                                animated=True,
                            ),
                        ),
                    ]
                )

        if random.random() < 0.1:
            message_parts = [
                ChatMessagePartRequest(
                    type='text',
                    text=f'@{random.choice(usernames)[1]} {message_parts[0].text}',
                )
            ]

        if random.random() < 0.1:
            await create_chat_message(
                ChatMessageCreate(
                    type='notice',
                    sub_type='sub',
                    channel_id=channel_id,
                    provider_viewer_id=provider_channel_id,
                    viewer_name=username,
                    viewer_display_name=display_name,
                    provider_message_id=str(uuid7()),
                    provider=provider,
                    provider_channel_id=provider_channel_id,
                    message_parts=message_parts,
                    badges=selected_badges,
                    notice_message=(
                        f'{display_name} subscribed at Tier {random.randint(1, 3)}. '
                        f"They've subscribed for {random.randint(2, 55)} months!"
                    ),
                )
            )
        else:
            await create_chat_message(
                ChatMessageCreate(
                    type='message',
                    channel_id=channel_id,
                    provider_viewer_id=provider_channel_id,
                    viewer_name=username,
                    viewer_display_name=display_name,
                    provider_message_id=str(uuid7()),
                    provider=provider,
                    provider_channel_id=provider_channel_id,
                    message_parts=message_parts,
                    badges=selected_badges,
                )
            )
        if wait_after_message:
            await asyncio.sleep(wait_after_message)
