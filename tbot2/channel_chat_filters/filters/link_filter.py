import re
import sys
from typing import Literal
from uuid import UUID

from async_lru import alru_cache

from tbot2.common import ChatMessage

from ..actions.link_allow_actions import (
    LinkAllow,
)
from ..actions.link_allow_actions import (
    get_link_allowlist as get_link_allowlist,
)
from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseUpdate,
    ChatFilterName,
    ChatFilterTimeoutMessage,
    ChatFilterWarningMessage,
    FilterMatchResult,
)


class ChatFilterLinkCreate(ChatFilterBaseCreate):
    type: Literal['link']
    name: ChatFilterName = 'Link Filter'
    warning_message: ChatFilterWarningMessage = (
        'You are not permitted to post links [warning]'
    )
    timeout_message: ChatFilterTimeoutMessage = 'You are not permitted to post links'


class ChatFilterLinkUpdate(ChatFilterBaseUpdate):
    type: Literal['link']


class ChatFilterLink(ChatFilterBase):
    type: Literal['link']

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        matches = RE_URL.findall(message.message_without_fragments())
        if not matches:
            return FilterMatchResult(filter=self, matched=False)
        allowlist = await get_link_allowlist_cached(filter_id=self.id)
        for match in matches:
            for allow in allowlist:
                if match[2] in allow.url:
                    return FilterMatchResult(filter=self, matched=False)
        return FilterMatchResult(filter=self, matched=True)


@alru_cache(ttl=1, maxsize=1000 if 'pytest' not in sys.modules else 0)
async def get_link_allowlist_cached(
    filter_id: UUID,
) -> list[LinkAllow]:
    return await get_link_allowlist(filter_id)


RE_URL = re.compile(
    "((?:(http|https|rtsp):\\/\\/(?:(?:[a-z0-9\\$\\-\\_\\.\\+\\!\\*\\'\\(\\)"
    '\\,\\;\\?\\&\\=]|(?:\\%[a-fA-F0-9]{2})){1,64}(?:\\:(?:[a-z0-9\\$\\-\\_'
    "\\.\\+\\!\\*\\'\\(\\)\\,\\;\\?\\&\\=]|(?:\\%[a-fA-F0-9]{2})){1,25})?\\@)?)?"
    '((?:(?:[a-z0-9][a-z0-9\\-]{0,64}\\.)+'
    '(?:'
    '(?:(?:NORTHWESTERNMUTU|INTERNATION|LPLFINANCI|(?:PRUDENT|MEMOR)I|FINANCI|SOCI|MUTU|TOT)A|(?:WILLIAMHI|HONEYWE|TMA|SHE)L|BAS(?:KET|E)BAL|ISTANBU|HOSPITA|FOOTBAL|(?:HOTMA|LIX|GMA)I|D(?:IGITA|ENTA|H)|S(?:CHOO|AR)|GLOBA|FUTBO|CHANE|(?:TIR|U)O|LEGA|EMAI|POH|LID|JL)L|(?:(?:(?:TRAVELERS|LIFE)INSURAN|E(?:XTRASPA|SURAN)|(?:INSURA|SCIE)N|RELIAN|OFFI|SPA|DAN)C|(?:RIGHTATHO|SHOWTI|LANCO|PRI)M|B(?:RIDGESTON|OUTIQU|LU|IK)|(?:PROGRESS|DR)IV|(?:ONYOUR|WOOD)SID|NA(?:TIONWID|M)|(?:C(?:APITALO|OLOG)|MELBOUR|ONLI|ZO)N|REALESTAT|(?:HEALTHC|SOFTW)AR|HO(?:MESEN|[RU])S|(?:FIRE|RED)STON|(?:LIFESTY|F(?:IRMD|ORS)A|S(?:CHU|TY|MI)|ORAC|CIRC|BIB)L|(?:INSTITU|DELOIT|WEBSI)T|FURNITUR|(?:MORTGA|EXCHAN|STORA|ORAN|VOYA|GEOR|DOD)G|CLINIQU|T(?:HEATR|UB)|METLIF|YOUTUB|L(?:ATROB|I(?:ND|K)|OV)|C(?:O(?:MPAR|LLEG|FFE)|H(?:ROM|AS)|BR|AF)|LASALL|KINDL|DEGRE|GOOGL|ESTAT|S(?:KYP|IT|AV)|P(?:LAC|HON|AG)|LEAS|G(?:U(?:ID|G)|RIP|LAD|GE)|IEE|FAG|WM)E|(?:(?:KERRYPROPERTI|MOTORCYCL|ENTERPRIS|P(?:ROPERTI|ICTUR)|INDUSTRI|LADBROK|SERVIC|SUPPLI|VENTUR|RECIP|S(?:TAP|ING)L|CO(?:URS|D)|VIAJ|H(?:UGH|ERM)|TUN)E|KERRYLOGISTIC|SCHOLARSHIP|(?:CONTRACTO|TATAMOTO|(?:PARTN|WINN|ROG)E|GUITA|FLOWE|TOU)R|KERRYHOTEL|(?:P(?:RODUCTIO|ASSAGE)|(?:VACA|SOLU)TIO|FROGA)N|INVESTMENT|B(?:NPPARIBA|UILDER|RUSSEL|ARGAIN|EAT)|HOMEGOOD|FAIRWIND|(?:MARSHAL|RENTA|TOO)L|(?:CHRISTM|V(?:ILL|EG))A|H(?:O(?:LDING|TELE)|AU)|D(?:IAMON)?D|(?:CITYEA|TICKE|FLIGH|YACH|EVEN|BOA)T|GRAPHIC|(?:BUSIN|LANX|FITN|EXPR)ES|W(?:INDOW|A(?:TCH|L)E)|P(?:HILIP|ARI)|SYSTEM|FARMER|ORIGIN|DOMAIN|TENNI|G(?:RATI|LAS|IVE)|(?:ZAPP|VUEL|JUEG)O|C(?:ONDO|LAIM|ARD)|TI(?:RE|P)|S(?:WIS|UCK|HOE)|ROCK|NEXU|MACY|L(?:OCU|D)|PRES|JPR|UP)S|(?:(?:(?:SANDVIKCOROM|RESTAUR)A|VISTAPRI|MANAGEME|GOLDPOI|EQUIPME)N|(?:NEXTDIR|UCONN|ISEL|SEL)EC|M(?:ICROSOF|EE)|HOMEDEPO|(?:ETISAL|IMAM)A|D(?:I(?:SCOUN|E)|EMOCRA|UPON)|BAREFOO|(?:BUDAPE|FLORI|DENTI|COMCA|TRU|EPO)S|S(?:CHMID|POR)|HANGOU|(?:WALMA|S(?:UPPO|MA)|REPO)R|C(?:RICKE|ONTAC)|P(?:ICTE|OS)|INTUI|EXPER|(?:TAR|PIA)GE|QUES|JETZ|L(?:OF|GB)|RMI|FIA|NT)T|A(?:(?:MERICANEXPRES|SSOCIATE|PARTMENT|NALYTIC)S|(?:MERICANFAMIL|FAMILYCOMPAN|TTORNE|LIPA|GENC|RM)Y|C(?:COUNTANTS|ADEMY|TOR|O)|C(?:COUNTANT)?|M(?:STERD|F)AM|L(?:L(?:FINANZ|Y)|STOM)|(?:LFAROME|RAMC|ER)O|(?:(?:QUAREL|UDIB|PP)L|C(?:CENTUR|TIV)|LLSTAT|IRFORC|LSAC|ZUR)E|B(?:UDHABI|OGADO|B(?:VIE|OTT)|ARTH|LE|C)|N(?:DROID|Z)|(?:UCTIO|KD)N|GAKHAN|(?:THLET|LIBAB|(?:VIAN|MI)C|FRIC|S[DI]|RP)A|(?:USPOS|DUL)T|I(?:R(?:TEL|BUS)|GO)|NQUAN|UTHOR|UDIO|E(?:TNA|G)|(?:UTO|W)S|RCHI|U(?:DI)?|UTO|R(?:TE|AB)|MEX|D(?:AC|S)|A(?:RP|A)|RT?|PP|IG?|BB|XA|OL|FL|[XZ]|T|S|Q|O|M|L|G|F|E|D|W)|(?:WEATHERCHANN|C(?:OOKINGCHANN|ITAD|HANN)|TRAVELCHANN|MATT)EL|(?:BANANAREPUBLI|(?:PANASO|ORGA)NI|(?:SYMANT|QUEB)E|CATHOLI|L(?:ECLER|L)|C(?:OMSE|S)|ICB|HSB|QV|NY)C|(?:C(?:A(?:NCERRESEARC|SEI)|(?:HUR|OA)C)|(?:ZUERI|S(?:WAT|EAR))C|MONAS|RICO|IRIS|FAIT|BOSC|GMB|OV|KF)H|(?:(?:(?:(?:SPREADBET|LIGH)T|SHOPP|PLUMB|TRAIN|WEDD|VIK|RAC)I|V(?:ERSICHERU|OTI)|C(?:ONSULT|L(?:OTH|EAN)|ATER)I|MARKETI|SAMSU|TRADI|LIVI|GIVI|DATI)N|(?:ENGINEER|HOST|GENT|FISH|SL)IN|KPM|DVA)G|(?:(?:W(?:OLTERSKLUW|ALT)|SWIFTCOV|SCHAEFFL|L(?:A(?:NDROV|WY)|OCK)|OBSERV|FRONTI|DISCOV|C(?:HRYSL|ARTI)|GRAING|P(?:IONE|FIZ|OK)|JUNIP|S(?:OCC|EN)|ROCH|KOSH)E|B(?:LOCKBUST|OEHRING|RO(?:TH|K)|E)E|LANCASTE|(?:FRONTDO|DOCT)O|(?:MO(?:VIST|P)|NEUST|JAGU)A|GOODYEA|(?:C(?:OMPU|EN)|MONS)TE|(?:THEAT|WEB)E|R(?:E(?:ALTO|PAI)|UH)|KINDE|F(?:LICK|T)|D(?:EALE|ABU)|S(?:OLA|F)|LAME|HAI)R|(?:(?:CONSTRUC|(?:PLAYST|FOUND|EDUC)A|PROTEC)TIO|(?:CALVINKLE|VIRG|LUP)I|(?:CREDITUN|EUROVIS|FASH)IO|(?:V(?:OLKSWAG|LAANDER)|IMMOBILI|K(?:ITCH|AUF)|SEV|OP)E|(?:(?:SCJOHN|LIAI)S|E(?:RICS|P)S|VISI|M(?:ORM|AIS)|LOND|QP)O|VERISIG|C(?:A(?:PETOW|NO)|ROW|ER)|LINCOL|YAMAXU|N(?:ORT|IK)O|G(?:ARD|RE)E|D(?:ESIG|ATSU)|B(?:OSTO|ERLI|AYER)|SALO|KOEL|WIE|TOW|POR|YU)N|(?:FOODNETWOR|(?:S(?:TATE|OFT)|HDFC|EVER|NET)BAN|(?:LUNDBE|FEEDBA)C|C(?:OMMBAN|LIC)|T(?:EMASE|AL)|NETWOR|LEFRA|EMERC|UBAN|S(?:IL|EE)|D(?:UC|CL)|NH)K|(?:B(?:ARCLAYCAR|ON)|NEWHOLLAN|(?:CREDITC|VANGU)AR|SAARLAN|MERCKMS|DOWNLOA|(?:LIMIT|EXPOS)E|CL(?:UBME|OU)|WORL|RAI|KRE)D|(?:REDUMBRELL|C(?:UISINELL|AMER)|(?:TELEFON|PRAMER|CORS)IC|SHANGRIL|YO(?:KOHAM|G)|IPIRANG|S(?:HIKSH|TAD)|OKINAW|LA(?:CAIX|NCI)|TOSHIB|T(?:I(?:END|A)|EV)|N(?:AGOY|OKI|INJ|B)|(?:O(?:TSU|SA)|VOD)K|(?:SAK|NAT)UR|TOYOT|PIZZ|M(?:EDI|OD|B)|OMEG|HOND|EDEK|D(?:ELT|OH)|ZAR|JAV|B(?:OF|BV))A|(?:PHOTOGRAPH|(?:B(?:LACKFRID|ROADW)|HOLID|TO[DR])A|TECHNOLOG|(?:UNIVERS|C(?:OMMUN|HAR)|SECUR|FIDEL|XFIN)IT|(?:D(?:IRECTO|ELIVE)|JEWEL|GALLE|(?:SURG|GROC)E|LUXU)R|(?:MCKINS|BENTL|HOCK)E|PHARMAC|OLDNAV|GODADD|CO(?:UNTR|MPAN)|B(?:E(?:STBU|AUT)|AB)|TIFFAN|SAFET|ENERG|SYDNE|FAMIL|RUGB|MONE|LIPS|LILL|NAV)Y|(?:LAMBORGHIN|(?:(?:MITSUBI|YODOBA)S|HITAC)H|RICHARDL|HELSINK|C(?:IPRIAN|HINTA)|(?:MASERA|INFINI)T|ISMAIL|F(?:ERRAR|Y)|(?:HYUND|DUB)A|B(?:UGAT|HAR)T|TAIPE|S(?:HOUJ|ANOF)|SUZUK|PRAX|MIAM|GUCC|WIK|K(?:IW|DD)|ERN)I|(?:(?:OLAYAN|STC)GROU|KUOKGROU|MAKEU|G(?:ALL|RO)U|HIPHO|D(?:UNLO|N)|SHAR|CHEA|RSV|JEE)P|(?:REPUBLIC|JPMORG|GUARDI|CARAV|WARM|DURB|XIHU)AN|T(?:R(?:AVEL(?:ERS)?)?|E(?:CH|L)|AX|O|M|K|J|H|D|C)|(?:F(?:UJIXERO|ORE)|NETFLI|(?:T[JK]MA|X)X|XERO|XBO)X|(?:(?:HISAMI|KOMA)TS|WANGGO|FUJITS|RYUKY|TUSH|CY(?:MR|O)|SOH|ITA|GUR)U|B(?:LO(?:OMBER)?G|A(?:RCLAYS|N(?:AMEX|[DK])|IDU)|OOKING|O(?:STIK|[MTX])|ZH|UY|NL|M[SW]|I[DOZ]|ET|C[GN]|B[CT]|[DFGJSTVWY])|(?:ST(?:OCKHOL|ATEFAR)|(?:S(?:HRIR|TRE)|WEBC)A|MUSEU|F(?:ORU|IL)|TEA|ROO|I[BF])M|(?:FRESENI|BAUHA|LEX)US|BARCELONA|ENGINEER|P(?:RO(?:PERTY|F)|H(?:OTOS|D)|A(?:R(?:T[SY]|S)|Y)|LUS|I(?:N[GK]|CS|D)|[GKMSTY])|(?:S(?:AMSCL|TARH)U|REHA|PU)B|(?:(?:B(?:RADES|LAN)|IVE|CIS)C|W(?:HOSWH|EIB)|FERRER|T(?:A(?:TTO|OBA)|OKY)|S(?:TUDI|AX)|P(?:HYSI|ROM)|(?:LATI|IKA)N|CASIN|ZIPP|VOLV|YAHO|RADI|MANG|KYOT|(?:VI|RO)DE|O(?:LL|O)|NIC|ZER|JI|HB)O|(?:MARRIO|HYA)TT|S(?:A(?:NDVIK|FE)?|T(?:AR)?|H(?:O[PW])?|KY?|EX?|[UY]|R|O|N|M|I|C|B)|WEATHER|C(?:O(?:OKING|M)?|A(?:PITAL|SE|RE?|T|M|L)?|R(?:EDIT)?|L(?:UB)?|I(?:T[IY])?|[UY]|H|F)|M(?:A(?:RKETS|IF|P)|O(?:SCOW|BIL[EY]|VIE|[EIM])|I(?:N[IT]|L)|E(?:NU|ME)|T[NR]|L[BS]|[DGHKNP-RV-Z])|F(?:I(?:NA(?:NCE|L)|DO)|UND|R(?:EE|L)|O(?:RD|X)|L(?:IR|Y)|A(?:ST|IL)|[JKM])|(?:HAM|JO)BURG|(?:SCHWAR|NOWRU|GBI|BUZ|XY)Z|(?:REVIEW|C(?:RUISE|OUPON|AREER)|WORK|GAME|LOAN|FAN|TV)S|POLITIE|(?:REXRO|EAR)TH|O(?:LAYAN|RG|NL|FF|M)|M(?:A(?:RKET|N)?|O(?:TO|BI|V)?|IT|E(?:N|D)?|[TU]|L|C)|H(?:EALTH|O(?:MES|T)|DFC|U|K)|D(?:IRECT|E(?:SI|AL)?|O)|REVIEW|C(?:RUISE|OUPON|AREER)|S(?:E(?:CURE|XY|AT|[SW])|T(?:UDY|ORE)|URF|POT|O(?:N[GY]|Y)|NCF|INA|H(?:IA|AW)|C(?:O[RT]|[AB])|R[LT]|B[IS]|A[PS]|[DGJSVXZ])|R(?:E(?:A(?:LTY|D)|IT)|UN|I[LOP])|SUPPLY|N(?:I(?:SSA[NY]|KE)|E(?:WS|C)|R[AW]|AB|[CLPUZ])|I(?:N(?:SURE|TEL|FO|[CGK])|MDB|TV|C[EU]|[DLOQ])|H(?:O(?:TELS|W)|E(?:RE|LP)|KT|IV|[MNRT])|(?:REISE|SKI)N|C(?:LINIC|ITIC|OO[LP]|HAT|A(?:S[AH]|RS|MP|LL|B)|RS|F[AD]|E[BO]|B[ANS]|[CDGKMNV-XZ])|(?:YAN|NA|FE)DEX|MADRID|UNICOM|W(?:A(?:TCH|NG)|IN|ED)|P(?:H(?:OTO)?|R(?:OD?|U)?|L(?:AY)?|IN|F|A)|REISE|B(?:UILD|LACK|O(?:OK?)?|E(?:ST)?|AR?|Z|R|N|M|I|H|B)|T(?:A(?:TAR|XI|B)|O(?:YS|P)|UI|RV|JX|HD|DK|CI|[FGLNTWZ])|TRADE|L(?:O(?:TT[EO]|L)|UXE|I(?:VE|NK|MO)|[BCKRSVY])|G(?:L(?:OBO|E)|A(?:LLO|P)|O(?:LF|[PTV])|M[OX]|EA|DN|[FHNPQSTWY])|(?:NOW|HG)TV|D(?:E(?:ALS|LL|V)|UNS|O(?:CS|[GT])|I(?:SH|Y)|A(?:T[AE]|[DY])|VR|TV|[JKMZ])|(?:BING|NG|EC)O|GIFTS|R(?:ICH|E(?:ST|NT?|D)?|[OSU])|N(?:E(?:XT|W|T)?|OW?|R|I|A)|L(?:I(?:FE)?|A(?:ND|W|T)?|PL|[TU])|I(?:M(?:MO)?|ST?|NT?|T|R)|G(?:O(?:LD|O)|AL?|[RU]|M|L|I|G|E|D|B)|F(?:O(?:OD?)?|I(?:RE|T)?|UN|R)|FARM|HOST|GENT|FISH|GOOG|BING|WORK|GAME|LOAN|GIFT|W(?:INE|EIR|T[CF]|OW|[FS])|V(?:OT[EO]|I(?:V[AO]|SA|[GNP])|ANA|ET|[CGN])|SALE|PCCW|J(?:O(?:BS|[TY])|NJ|MP|C[BP])|LEGO|(?:LTD|MM)A|Z(?:IP|A)|YOU|STC|SKI|E(?:DU|[R-U])|LTD|FAN|XIN|U(?:NO|BS|[AGKSYZ])|O(?:TT|N[EG]|BI)|K(?:RD|PN|I[AM]|[GHMNWZ])|PET|MSD|E(?:US|SQ|AT|[EG])|P[NW]C|RWE|NFL|V[AEIU]|K[EIPRY]|J[EMOP]|PE|IE|MS|P[NW]|SL|MM|RW|NF|NG|EC|TV|Z[MW]|Y[ET]|QA'
    '))'
    '|(?:(?:25[0-5]|2[0-4]'
    '[0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9])\\.(?:25[0-5]|2[0-4][0-9]'
    '|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(?:25[0-5]|2[0-4][0-9]|[0-1]'
    '[0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}'
    '|[1-9][0-9]|[0-9])))'
    '(?:\\:\\d{1,5})?)'
    '(\\/(?:(?:[a-z0-9\\;\\/\\?\\:\\@\\&\\=\\#\\~'
    "\\-\\.\\+\\!\\*\\'\\(\\)\\,\\_])|(?:\\%[a-fA-F0-9]{2}))*)?"
    '(?:\\b|$)'
    r'|(\\.[a-z]+\\/|magnet:\/\/|mailto:\/\/|ed2k:\/\/|irc:\/\/|ircs:\/\/|skype:\/\/|ymsgr:\/\/|xfire:\/\/|steam:\/\/|aim:\/\/|spotify:\/\/)',
    re.IGNORECASE,
)
