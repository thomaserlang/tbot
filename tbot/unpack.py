import logging
from bottom import unpack

def unpack_command(msg):
    prefix, command, params = unpack.split_line(msg.strip())
    command = unpack.synonym(command)
    kwargs = {}  # type: Dict[str, Any]
    if command in ["PING", "PONG", "ERR_NOMOTD"]:
        kwargs["message"] = params[-1]

    elif command in ["PRIVMSG", "NOTICE", "WHISPER"]:
        unpack.nickmask(prefix, kwargs)
        kwargs["target"] = params[0]
        kwargs["message"] = params[-1]

    elif command in ["JOIN"]:
        unpack.nickmask(prefix, kwargs)
        kwargs["channel"] = params[0]

    elif command in ["NICK"]:
        unpack.nickmask(prefix, kwargs)
        kwargs["new_nick"] = params[0]

    elif command in ["RPL_NAMREPLY"]:
        kwargs["target"] = params[0]
        if len(params) > 3:
            kwargs["channel_type"] = params[1]
        else:
            kwargs["channel_type"] = None
        kwargs["channel"] = params[-2]
        kwargs["users"] = params[-1].split(" ")

    elif command in ["RPL_WHOREPLY"]:
        """ 352 RPL_WHOREPLY
              <channel> <user> <host> <server> <nick>
              ( "H" / "G" > ["*"] [ ( "@" / "+" ) ]
              :<hopcount> <real name>"
        """
        (kwargs["target"],
         kwargs["channel"],
         kwargs["user"],
         kwargs["host"],
         kwargs["server"],
         kwargs["nick"],
         kwargs["hg_code"]) = params[0:7]
        hc, kwargs["real_name"] = params[-1].split(" ", 1)
        kwargs["hopcount"] = int(hc)

    elif command in ["RPL_ENDOFWHO"]:
        kwargs["name"] = params[0]
        kwargs["message"] = params[1]

    elif command in ["QUIT"]:
        unpack.nickmask(prefix, kwargs)
        if params:
            kwargs["message"] = params[0]
        else:
            kwargs["message"] = ""

    elif command in ["PART"]:
        unpack.nickmask(prefix, kwargs)
        kwargs["channel"] = params[0]
        if len(params) > 1:
            kwargs["message"] = params[-1]
        else:
            kwargs["message"] = ""

    elif command in ["INVITE"]:
        unpack.nickmask(prefix, kwargs)
        kwargs["target"] = params[0]
        kwargs["channel"] = params[1]

    elif command in ["RPL_TOPIC", "RPL_NOTOPIC", "RPL_ENDOFNAMES"]:
        kwargs["channel"] = params[1]
        kwargs["message"] = params[2]

    elif command in ["RPL_MOTDSTART", "RPL_MOTD", "RPL_ENDOFMOTD",
                     "RPL_WELCOME", "RPL_YOURHOST", "RPL_CREATED",
                     "RPL_LUSERCLIENT", "RPL_LUSERME"]:
        kwargs["message"] = params[-1]

    elif command in ["RPL_LUSEROP", "RPL_LUSERUNKNOWN", "RPL_LUSERCHANNELS"]:
        kwargs["count"] = int(params[1])
        if len(params) > 2:
            kwargs["message"] = params[-1]
        else:
            kwargs["message"] = ""

    elif command in ["RPL_MYINFO", "RPL_BOUNCE"]:
        kwargs["info"] = params[1:-1]
        kwargs["message"] = params[-1]

    elif command in ["TOPIC"]:
        kwargs["channel"] = params[0]
        if len(params) > 1:
            kwargs["message"] = params[1]
        else:
            kwargs["message"] = ""

    elif command in ["MODE"]:
        unpack.nickmask(prefix, kwargs)
        if params[0][0] in "&#!+":
            command = "CHANNELMODE"
            kwargs["channel"] = params[0]
            kwargs["modes"] = params[1]
            if len(params) > 2:
                kwargs["params"] = params[2:]
            else:
                kwargs["params"] = []
        else:
            command = "USERMODE"
            kwargs["nick"] = params[0]
            kwargs["modes"] = params[1]

    elif command in ["CLEARCHAT"]:
        kwargs['channel'] = params[0]
        kwargs['banned_user'] = params[1] if len(params) >= 2 else None


    elif command in ["USERNOTICE"]:
        kwargs['channel'] = params[0]
        kwargs['message'] = params[1].strip() if len(params) >= 2 else None

    else:
        raise ValueError("Unknown command '{}'".format(command))

    return command, kwargs

def rfc2812_handler(client):
    async def handler(next_handler, message):
        twitchextra = {}
        if message.startswith('@'):
            te, message = message.split(' ', 1)
            for e in te[1:].split(';'):
                a = e.split('=', 1)
                twitchextra[a[0]] = a[1].replace('\\s', ' ') if len(a) == 2 else ''
        try:
            event, kwargs = unpack_command(message)
            kwargs.update(twitchextra)
            client.trigger(event, **kwargs)
        except ValueError:
            logging.debug("Failed to parse line >>> {}".format(message))
        await next_handler(message)
    return handler
