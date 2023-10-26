import re, collections, doctest

def get_user_agent(log: str) -> str:
    """
    Get the user agent of the line.

    Expamples
    ---------
    Expamples
    ---------
    >>> get_user_agent('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    >>> get_user_agent('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
    """

    log_compile = re.compile(r'\"(\w+/\d.+)\"$')
    buscador = log_compile.findall(log)
    return buscador[0]

def is_bot(log: str) -> bool:
    '''
        Check of the access in the line correspons to a bot

        Examples
        --------
        >>> is_bot('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
        False

        >>> is_bot('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
        True

        >>> is_bot('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
        True
        '''
    bot_ = log.lower()
    if 'bot' in bot_:
        return True
    else:
        return False


def get_hour(log: str) -> int:
    """
        Get the user agent of the line.

        Expamples
        ---------
        >>> get_hour('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
        0

        >>> get_hour('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antacres.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
        12
        """

    dataere = re.compile(r':(\d+)')
    m = dataere.findall(log)
    return int(m[0])


def get_ipaddr(log):
    '''
    Gets the IP address of the line

    >>> get_ipaddr('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    '213.180.203.109'

    >>> get_ipaddr('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    '147.96.46.52'
    '''

    ip_compile = re.compile(r'(\d+.\d+.\d+.\d+).-')
    address = ip_compile.findall(log)
    return address[0]


def ipaddreses(log: str) -> set[str]:
    '''
    Returns the IPs of the accesses that are not bots
    '''

    with open('access_short.log') as f:
        for x in f:
            if is_bot(x) == False:
                return get_ipaddr(x)


def histbyhour(filename: str) -> dict[int, int]:
    '''
    Computes the histogram of access by hour
    '''

    lista_logs = list()
    with open('access_short.log') as f:
        for x in f:
            lista_logs.append(get_hour(x))
        count_per_hour = collections.Counter(lista_logs)
        return count_per_hour




def test_doc():
    doctest.run_docstring_examples(get_user_agent, globals(), verbose=True)
    doctest.run_docstring_examples(is_bot, globals(), verbose=True)
    doctest.run_docstring_examples(get_hour, globals(), verbose=True)
    doctest.run_docstring_examples(get_ipaddr, globals(), verbose=True)

def test_ipaddresses():
    assert ipaddreses('access_short.log') == {'34.105.93.183', '39.103.168.88'}

    def test_hist():
        hist = histbyhour('access_short.log')
        assert hist == {5: 3, 7: 2, 23: 1}