from parser import *
from lexer import *

def TestGetLr1Table():
    print('TEST: generate LR(1) table')
    testLang = 'test01'
    tokenPattern = GetTokenPattern(f'pattern/{testLang}.json')
    tokenList = GetTokenList(tokenPattern)
    testLang = 'test01'
    _, collToId, lr1Table = GetLr1TableFromGrammarFile(f'grammar/{testLang}.txt', tokenList)
    VisualizeLr1Table(lr1Table, collToId, f'table/{testLang}.csv')
    print(f'generated LR(1) table at table/{testLang}.csv')
    print()

def TestParse(testCase: str):
    print('TEST: parse code')
    testLang = 'toylang'
    code = ''
    with open(f'code/{testCase}.txt', 'r') as file:
        code = file.read()
    tokenPattern = GetTokenPattern(f'pattern/{testLang}.json')
    tokenRegex = GetTokenRegex(tokenPattern)
    tokenStream = Tokenize(code, tokenRegex)
    tokenList = GetTokenList(tokenPattern)
    start, _, lr1Table = GetLr1TableFromGrammarFile(f'grammar/{testLang}.txt', tokenList)
    ast = GetAst(tokenStream, lr1Table, start)
    xmlAst = ConvertAstToXml(ast)
    with open(f'tree/{testLang}-{testCase}.xml', 'w') as file:
        file.write(xmlAst)
    print(f'generated AST at tree/{testLang}-{testCase}.xml')
    print()

if __name__ == '__main__':
    TestGetLr1Table()
    import os
    testSrcDir = 'code'
    outputDir = 'tree'
    for root, dirs, files in os.walk(testSrcDir):
        for filename in files:
            TestParse(os.path.splitext(filename)[0])