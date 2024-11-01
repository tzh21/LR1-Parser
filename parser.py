from queue import Queue
from myutils import *
from itertools import count

def GetTerminalSet(tokenList: list[str]):
    terminalSet = set(tokenList)
    terminalSet.add(EOF_SYMBOL)
    return terminalSet

'''读取语法规则文件'''
def GetGrammar(grammerFile: str) -> str:
    with open(grammerFile, 'r') as file:
        return file.read()
    return None

'''根据语法规则计算开始符号和产生式'''
def GetProductions(grammar: str) -> tuple[str, ProductionTable]:
    productionTable: ProductionTable = dict()
    lines = grammar.splitlines()
    startSymbol = None
    metStartSymbol = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # 跳过空行或注释
            continue
        
        lhs, rhsListStr = line.split("->")  # 拆分出左边和右边
        lhs = lhs.strip()  # 去掉两边空格
        rhsList = rhsListStr.split("|")  # 用 "|" 分隔多个推导式
        
        if lhs not in productionTable:
            productionTable[lhs] = []

        if not metStartSymbol:
            metStartSymbol = True
            startSymbol = lhs
        
        for rhs in rhsList:
            symbols = rhs.strip().split()  # 将右侧按空格分割成符号
            productionTable[lhs].append(symbols)

    productionTable[START_SYMBOL] = [[startSymbol]]
    return startSymbol, productionTable

def GetFirstSet(
    s: SymbolString, firstSet: dict[Symbol, set[Symbol]],
    terminalSet: set[str], productionTable: ProductionTable
) -> set[Symbol]:
    # 读缓存
    if len(s) == 1 and s[0] in firstSet:
        return firstSet[s[0]]
    firstSymbol: str = s[0]
    ans: set[str] = set()
    # 如果首个符号不是终结符，需要考虑该符号的 First 集
    if firstSymbol not in terminalSet:
        for rhs in productionTable[firstSymbol]:
            if rhs[0] != emptyString:
                ans = ans.union(GetFirstSet(
                    rhs, firstSet,
                    terminalSet, productionTable
                ))
            else:
                if len(s) != 1:
                    ans = ans.union(GetFirstSet(
                        s[1:], firstSet,
                        terminalSet, productionTable
                    ))
                else:
                    ans = ans.union({emptyString})
    # 如果首个符号是终结符，直接吸收入 First 集合
    else:
        ans = ans.union({firstSymbol})
    # 写缓存
    if len(s) == 1:
        firstSet[s[0]] = ans
    return ans

def GetClosure(
    coll: Collection, terminalSet: set[str],
    productionTable: ProductionTable, firstSet,
) -> Collection:
    # 维护未处理的项目的队列
    todoItemQueue: Queue[Item] = Queue()
    for item in coll:
        todoItemQueue.put(item)
    # 对于每个项目，如果句点后面是非终结符，搜索对应的产生式，并将新项目加入其中
    while not todoItemQueue.empty():
        item = todoItemQueue.get()
        if item.dotPos >= len(item.rhs): # 说明 dot 在字符串结尾，无法进行移进
            continue
        newLhs = item.rhs[item.dotPos]
        if newLhs not in terminalSet:
            suffix = item.rhs[item.dotPos + 1:].copy()
            suffix.append(item.lookahead) # 约定 lookahead 必然存在
            rhsList = productionTable[newLhs]
            firstSetOfSuffix = GetFirstSet(
                suffix, firstSet,
                terminalSet, productionTable
            )
            for rhs in rhsList:
                for lookahead in firstSetOfSuffix:
                    newItem = Item(newLhs, rhs.copy(), 0, lookahead)
                    if newItem not in coll:
                        coll.add(newItem)
                        todoItemQueue.put(newItem)
    return coll

'''根据产生式计算 LR(1) 表'''
def GetLr1Table(
    originalStartSymbol: str, terminalSet: set[str],
    productionTable: ProductionTable, firstSet,
) -> tuple[Collection, CollToId, Lr1Table]:
    lr1Table: dict = dict()
    # 创建初始 Collection
    startColl = Collection()
    startColl.add(Item(START_SYMBOL, [originalStartSymbol], 0, EOF_SYMBOL))
    startColl = GetClosure(startColl, terminalSet, productionTable, firstSet)
    # 构建集合到数字 id 的映射。数字 id 主要用于在可视化 LR(1) 表格中简化 Collection 的表示。
    idGen = count(0)
    collToId: CollToId = dict()
    collToId[frozenset(startColl)] = next(idGen)
    # 所有已创建的 Collection 的集合
    createdCollSet: set[Collection] = set()
    createdCollSet.add(frozenset(startColl))
    # 所有待处理的 Collection 的队列
    todoCollQueue: Queue[Collection] = Queue()
    todoCollQueue.put(frozenset(startColl))
    acceptedItem = Item(START_SYMBOL, [originalStartSymbol], 1, EOF_SYMBOL)
    # 逐个处理 Collection
    while not todoCollQueue.empty() > 0:
        coll = todoCollQueue.get()
        destCollMap: dict[Symbol, Collection] = dict()
        for item in coll:
            if item.dotPos > len(item.rhs):
                raise Exception('dot pos exceed length of rhs')
            if item.dotPos == len(item.rhs):
                if (coll, item.lookahead) in lr1Table:
                    raise(TableAlreadyFilledException())
                if item == acceptedItem:
                    lr1Table[(coll, item.lookahead)] = (Lr1Command.ACCEPT, '')
                    continue
                lr1Table[(coll, item.lookahead)] = (Lr1Command.REDUCE, (item.lhs, item.rhs.copy()))
                continue
            else:
                symbol = item.rhs[item.dotPos]
                if symbol not in destCollMap:
                    destCollMap[symbol] = Collection()
                newItem = Item(item.lhs, item.rhs.copy(), item.dotPos + 1, item.lookahead)
                destCollMap[symbol].add(newItem)
        for symbol in destCollMap:
            destColl = GetClosure(destCollMap[symbol], terminalSet, productionTable, firstSet)
            if len(destColl) == 0:
                raise(Exception('new collection was empty'))
            if symbol in terminalSet:
                if (coll, symbol) in lr1Table:
                    raise(TableAlreadyFilledException())
                lr1Table[(coll, symbol)] = (Lr1Command.SHIFT, frozenset(destColl))
            else:
                if (coll, symbol) in lr1Table:
                    raise(TableAlreadyFilledException())
                lr1Table[(coll, symbol)] = (Lr1Command.GOTO, frozenset(destColl))
            if destColl not in createdCollSet:
                collToId[frozenset(destColl)] = next(idGen)
                createdCollSet.add(frozenset(destColl))
                todoCollQueue.put(frozenset(destColl))
    return startColl, collToId, lr1Table

def GetLr1TableFromGrammarFile(grammarFile: str, tokenList: list[str]) -> tuple[Collection, CollToId, Lr1Table]:
    grammar = GetGrammar(grammarFile)
    originalStartSymbol, productionTable = GetProductions(grammar)
    terminalSet = GetTerminalSet(tokenList)
    firstSet = dict()
    return GetLr1Table(
        originalStartSymbol, terminalSet, productionTable, firstSet
    )

import pandas as pd
pd.set_option('display.max_colwidth', 1000)

def VisualizeCollection(coll: Collection, collToId: CollToId):
    print(collToId[coll])
    for item in coll:
        print(item)
    print()

def VisualizeAllCollections(collToId: CollToId):
    for coll in collToId:
        VisualizeCollection(coll, collToId)

def GetVisualizedAction(action: Action, collToId: CollToId) -> str:
    if action[0] == Lr1Command.SHIFT:
        return f'shift  {collToId[action[1]]}'
    elif action[0] == Lr1Command.GOTO:
        return f'goto   {collToId[action[1]]}'
    elif action[0] == Lr1Command.REDUCE:
        return f'reduce {action[1][0]} -> {' '.join(action[1][1])}'
    elif action[0] == Lr1Command.ACCEPT:
        return f'accept'
    else:
        raise(Exception('unknown command'))

def VisualizeLr1Table(lr1Table: Lr1Table, collToId: CollToId, outputFile: str):
    data = [(collToId[coll], symbol, f'{GetVisualizedAction(action, collToId)}') for (coll, symbol), action in lr1Table.items()]
    df = pd.DataFrame(data, columns=["State", "Symbol", "Action"])
    df = df.pivot(index="State", columns="Symbol", values="Action")
    df.to_csv(outputFile, index=True)

'''根据 LR(1) 表解析 token 流，得到抽象语法树'''
def GetAst(
    tokenStream: list[tuple[str, str]],
    lr1Table: Lr1Table,
    startColl: Collection,
) -> AstNode:
    tokenStream.append(EOF_SYMBOL)
    collStack: list[Collection] = list()
    collStack.append(frozenset(startColl))
    tokenIter = iter(tokenStream)
    token = next(tokenIter)
    nodeStack: list[AstNode] = list()
    # symbolStack.append(AstNode(token[0], True, token[1]))
    try:
        while True:
            state = collStack[-1]
            if (state, token[0]) not in lr1Table:
                raise(Exception('failed to parse'))
            command = lr1Table[(state, token[0])]
            if command[0] == Lr1Command.SHIFT:
                collStack.append(command[1])
                nodeStack.append(AstNode(token[0], True, token[1]))
                token = next(tokenIter)
            elif command[0] == Lr1Command.REDUCE:
                rhs: SymbolString = command[1][1]
                numPoped = len(rhs)
                collStack = collStack[:-numPoped]
                topColl = collStack[-1]
                pushedSymbol: Symbol = command[1][0]
                gotoCommand = lr1Table[(topColl, pushedSymbol)]
                collStack.append(gotoCommand[1])
                # 更新 Ast 节点栈
                popedNodeList = nodeStack[-numPoped:].copy()
                pushedNode = AstNode(pushedSymbol, False, popedNodeList)
                nodeStack = nodeStack[:-numPoped]
                nodeStack.append(pushedNode)
            elif command[0] == Lr1Command.ACCEPT:
                print('accepted')
                return nodeStack[-1]
            else:
                raise(Exception('unknown command'))
    except StopIteration:
        print('not accepted')

def ConvertAstToXml(ast: AstNode, indent = 0):
    symbol = ast.symbol
    children = ast.children
    isTerminal = ast.isTerminal
    
    indentation = ' ' * (indent * 4)
    
    if isTerminal:
        return f'{indentation}<{symbol}>{children}</{symbol}>'
    else:
        result = f'{indentation}<{symbol}>\n'
        for item in children:
            result += ConvertAstToXml(item, indent + 1) + '\n'
        result += f'{indentation}</{symbol}>'
        return result