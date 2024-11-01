import re
import json

def GetTokenPattern(filePath: str) -> list[(str, str)]:
    with open(filePath, 'r') as file:
        data = json.load(file)
    return [(item[0], item[1]) for item in data]

def GetTokenList(tokenPattern: list[tuple[str, str]]) -> list[str]:
    return [spec[0] for spec in tokenPattern]

def GetTokenRegex(tokenPattern: list[(str, str)]) -> str:
    return '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in tokenPattern)

'''词法分析器：将输入代码分解为 token 流'''
def Tokenize(code: str, tokenRegex: str) -> list[tuple[str, str]]:
    tokens = []
    for match in re.finditer(tokenRegex, code):
        kind = match.lastgroup
        value = match.group()
        tokens.append((kind, value))
    return tokens
