lr1Table = {
    ('a', 'b'): ('jump', 'c')
}

import pandas as pd
data = [(state, symbol, action) for (state, symbol), action in lr1Table.items()]
df = pd.DataFrame(data, columns=["State", "Symbol", "Action"]).fillna('-')
print(df)