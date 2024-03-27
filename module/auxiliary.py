import re
import time

def getTimestamp(ms: bool=False) -> int:
    return int(time.time() * (1000 if ms else 1))

def isUrl(text: str) -> bool:
    compile = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
    return bool(compile.search(text))

def base62Encode(number: int) -> str:
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if number == 0:
        return alphabet[0]
    results = []
    base = len(alphabet)
    while number:
        rem = number % base
        number = number // base
        results.append(alphabet[rem])
    results.reverse()
    return ''.join(results)