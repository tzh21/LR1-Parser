# 编译小作业1.4-Toy语言的LR(1)分析

## 运行方法

```bash
python test.py
```

这个命令会对任务一中的语法规则生成 CSV 格式的 LR(1) 分析表，会解析三个 ToyLang 源代码并生成 XML 格式的语法分析树。生成文件的位置见终端输出。

请用表格编辑工具（如 Microsoft Excel 或 Apple Numbers）打开 CSV 文件。（文本格式的 CSV 文件不易读）

## 运行结果

文档中的结果可能受制于篇幅限制。具体输出详见 `tree` 目录

01.txt

```
var n;
```

```xml
<PROGRAM>
    <STATEMENT>
        <DECLARATION_STMT>
            <var>var</var>
            <identifier>n</identifier>
            <semicolon>;</semicolon>
        </DECLARATION_STMT>
    </STATEMENT>
</PROGRAM>
```

02.txt

```
var x;
var y;
input x;
if (x > 5) {
    y = x * (x / 2 + 10);
}
print "After if, finished!";
```

```xml
<PROGRAM>
    <STATEMENT>
        <DECLARATION_STMT>
            <var>var</var>
            <identifier>x</identifier>
            <semicolon>;</semicolon>
        </DECLARATION_STMT>
    </STATEMENT>
    <PROGRAM>
        <STATEMENT>
            <DECLARATION_STMT>
                <var>var</var>
                <identifier>y</identifier>
                <semicolon>;</semicolon>
            </DECLARATION_STMT>
        </STATEMENT>
        <PROGRAM>
            <STATEMENT>
                <INPUT_STMT>
                    <input>input</input>
                    <identifier>x</identifier>
                    <semicolon>;</semicolon>
                </INPUT_STMT>
            </STATEMENT>
            <PROGRAM>
                <STATEMENT>
                    <IF_STMT>
                        <if>if</if>
                        <lparen>(</lparen>
                        <CONDITION>
                            <EXPRESSION>
                                <TERM>
                                    <FACTOR>
                                        <identifier>x</identifier>
                                    </FACTOR>
                                </TERM>
                            </EXPRESSION>
                            <CONDITION_SUFFIX>
                                <greater>></greater>
                                <EXPRESSION>
                                    <TERM>
                                        <FACTOR>
                                            <number>5</number>
                                        </FACTOR>
                                    </TERM>
                                </EXPRESSION>
                            </CONDITION_SUFFIX>
                        </CONDITION>
                        <rparen>)</rparen>
                        <lbrace>{</lbrace>
                        <PROGRAM>
                            <STATEMENT>
                                <ASSIGNMENT_STMT>
                                    <identifier>y</identifier>
                                    <assign>=</assign>
                                    <EXPRESSION>
                                        <TERM>
                                            <FACTOR>
                                                <identifier>x</identifier>
                                            </FACTOR>
                                            <TERM_SUFFIX>
                                                <multiply>*</multiply>
                                                <FACTOR>
                                                    <lparen>(</lparen>
                                                    <EXPRESSION>
                                                        <TERM>
                                                            <FACTOR>
                                                                <identifier>x</identifier>
                                                            </FACTOR>
                                                            <TERM_SUFFIX>
                                                                <divide>/</divide>
                                                                <FACTOR>
                                                                    <number>2</number>
                                                                </FACTOR>
                                                            </TERM_SUFFIX>
                                                        </TERM>
                                                        <EXPRESSION_SUFFIX>
                                                            <plus>+</plus>
                                                            <TERM>
                                                                <FACTOR>
                                                                    <number>10</number>
                                                                </FACTOR>
                                                            </TERM>
                                                        </EXPRESSION_SUFFIX>
                                                    </EXPRESSION>
                                                    <rparen>)</rparen>
                                                </FACTOR>
                                            </TERM_SUFFIX>
                                        </TERM>
                                    </EXPRESSION>
                                    <semicolon>;</semicolon>
                                </ASSIGNMENT_STMT>
                            </STATEMENT>
                        </PROGRAM>
                        <rbrace>}</rbrace>
                    </IF_STMT>
                </STATEMENT>
                <PROGRAM>
                    <STATEMENT>
                        <PRINT_STMT>
                            <print>print</print>
                            <PRINT_SUFFIX>
                                <string_literal>"After if, finished!"</string_literal>
                                <semicolon>;</semicolon>
                            </PRINT_SUFFIX>
                        </PRINT_STMT>
                    </STATEMENT>
                </PROGRAM>
            </PROGRAM>
        </PROGRAM>
    </PROGRAM>
</PROGRAM>
```

03.txt

```
var n;
var total;
n = 0;
total = 0;
while (n < 5) {
    total = total + n;
    n = n + 1;
}
if (total > 10) {
    print "Total is greater than 10!\n";
}
if (total < 11) {
    print "Total is 10 or less.";
}
```

```xml
<PROGRAM>
    <STATEMENT>
        <DECLARATION_STMT>
            <var>var</var>
            <identifier>n</identifier>
            <semicolon>;</semicolon>
        </DECLARATION_STMT>
    </STATEMENT>
    <PROGRAM>
        <STATEMENT>
            <DECLARATION_STMT>
                <var>var</var>
                <identifier>total</identifier>
                <semicolon>;</semicolon>
            </DECLARATION_STMT>
        </STATEMENT>
        <PROGRAM>
            <STATEMENT>
                <ASSIGNMENT_STMT>
                    <identifier>n</identifier>
                    <assign>=</assign>
                    <EXPRESSION>
                        <TERM>
                            <FACTOR>
                                <number>0</number>
                            </FACTOR>
                        </TERM>
                    </EXPRESSION>
                    <semicolon>;</semicolon>
                </ASSIGNMENT_STMT>
            </STATEMENT>
            <PROGRAM>
                <STATEMENT>
                    <ASSIGNMENT_STMT>
                        <identifier>total</identifier>
                        <assign>=</assign>
                        <EXPRESSION>
                            <TERM>
                                <FACTOR>
                                    <number>0</number>
                                </FACTOR>
                            </TERM>
                        </EXPRESSION>
                        <semicolon>;</semicolon>
                    </ASSIGNMENT_STMT>
                </STATEMENT>
                <PROGRAM>
                    <STATEMENT>
                        <WHILE_STMT>
                            <while>while</while>
                            <lparen>(</lparen>
                            <CONDITION>
                                <EXPRESSION>
                                    <TERM>
                                        <FACTOR>
                                            <identifier>n</identifier>
                                        </FACTOR>
                                    </TERM>
                                </EXPRESSION>
                                <CONDITION_SUFFIX>
                                    <less><</less>
                                    <EXPRESSION>
                                        <TERM>
                                            <FACTOR>
                                                <number>5</number>
                                            </FACTOR>
                                        </TERM>
                                    </EXPRESSION>
                                </CONDITION_SUFFIX>
                            </CONDITION>
                            <rparen>)</rparen>
                            <lbrace>{</lbrace>
                            <PROGRAM>
                                <STATEMENT>
                                    <ASSIGNMENT_STMT>
                                        <identifier>total</identifier>
                                        <assign>=</assign>
                                        <EXPRESSION>
                                            <TERM>
                                                <FACTOR>
                                                    <identifier>total</identifier>
                                                </FACTOR>
                                            </TERM>
                                            <EXPRESSION_SUFFIX>
                                                <plus>+</plus>
                                                <TERM>
                                                    <FACTOR>
                                                        <identifier>n</identifier>
                                                    </FACTOR>
                                                </TERM>
                                            </EXPRESSION_SUFFIX>
                                        </EXPRESSION>
                                        <semicolon>;</semicolon>
                                    </ASSIGNMENT_STMT>
                                </STATEMENT>
                                <PROGRAM>
                                    <STATEMENT>
                                        <ASSIGNMENT_STMT>
                                            <identifier>n</identifier>
                                            <assign>=</assign>
                                            <EXPRESSION>
                                                <TERM>
                                                    <FACTOR>
                                                        <identifier>n</identifier>
                                                    </FACTOR>
                                                </TERM>
                                                <EXPRESSION_SUFFIX>
                                                    <plus>+</plus>
                                                    <TERM>
                                                        <FACTOR>
                                                            <number>1</number>
                                                        </FACTOR>
                                                    </TERM>
                                                </EXPRESSION_SUFFIX>
                                            </EXPRESSION>
                                            <semicolon>;</semicolon>
                                        </ASSIGNMENT_STMT>
                                    </STATEMENT>
                                </PROGRAM>
                            </PROGRAM>
                            <rbrace>}</rbrace>
                        </WHILE_STMT>
                    </STATEMENT>
                    <PROGRAM>
                        <STATEMENT>
                            <IF_STMT>
                                <if>if</if>
                                <lparen>(</lparen>
                                <CONDITION>
                                    <EXPRESSION>
                                        <TERM>
                                            <FACTOR>
                                                <identifier>total</identifier>
                                            </FACTOR>
                                        </TERM>
                                    </EXPRESSION>
                                    <CONDITION_SUFFIX>
                                        <greater>></greater>
                                        <EXPRESSION>
                                            <TERM>
                                                <FACTOR>
                                                    <number>10</number>
                                                </FACTOR>
                                            </TERM>
                                        </EXPRESSION>
                                    </CONDITION_SUFFIX>
                                </CONDITION>
                                <rparen>)</rparen>
                                <lbrace>{</lbrace>
                                <PROGRAM>
                                    <STATEMENT>
                                        <PRINT_STMT>
                                            <print>print</print>
                                            <PRINT_SUFFIX>
                                                <string_literal>"Total is greater than 10!\n"</string_literal>
                                                <semicolon>;</semicolon>
                                            </PRINT_SUFFIX>
                                        </PRINT_STMT>
                                    </STATEMENT>
                                </PROGRAM>
                                <rbrace>}</rbrace>
                            </IF_STMT>
                        </STATEMENT>
                        <PROGRAM>
                            <STATEMENT>
                                <IF_STMT>
                                    <if>if</if>
                                    <lparen>(</lparen>
                                    <CONDITION>
                                        <EXPRESSION>
                                            <TERM>
                                                <FACTOR>
                                                    <identifier>total</identifier>
                                                </FACTOR>
                                            </TERM>
                                        </EXPRESSION>
                                        <CONDITION_SUFFIX>
                                            <less><</less>
                                            <EXPRESSION>
                                                <TERM>
                                                    <FACTOR>
                                                        <number>11</number>
                                                    </FACTOR>
                                                </TERM>
                                            </EXPRESSION>
                                        </CONDITION_SUFFIX>
                                    </CONDITION>
                                    <rparen>)</rparen>
                                    <lbrace>{</lbrace>
                                    <PROGRAM>
                                        <STATEMENT>
                                            <PRINT_STMT>
                                                <print>print</print>
                                                <PRINT_SUFFIX>
                                                    <string_literal>"Total is 10 or less."</string_literal>
                                                    <semicolon>;</semicolon>
                                                </PRINT_SUFFIX>
                                            </PRINT_STMT>
                                        </STATEMENT>
                                    </PROGRAM>
                                    <rbrace>}</rbrace>
                                </IF_STMT>
                            </STATEMENT>
                        </PROGRAM>
                    </PROGRAM>
                </PROGRAM>
            </PROGRAM>
        </PROGRAM>
    </PROGRAM>
</PROGRAM>
```