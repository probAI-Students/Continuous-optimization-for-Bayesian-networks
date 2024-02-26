import pandas as pd
import os
import networkx as nx
from pyvis.network import Network
from causalnex.structure.dynotears import from_pandas_dynamic

all_files = []

for root, dirs, files in os.walk(r"SKAB/data"):
    for file in files:
        if file.endswith(".csv"):
            all_files.append(os.path.join(root, file))
dfs = []

for path in all_files:
    df = pd.read_csv(path, index_col='datetime', sep=';', parse_dates=True).reset_index(drop=True)
    dfs.append(df)
print(len(dfs))
# dfs=[]
# for path in all_files:
#     if 'valve2' in path:
#         df = pd.read_csv(path,index_col='datetime',sep=';',parse_dates=True)
#         dfs.append(df)
#         print(len(df),df.index[-1]-df.index[0])
#         plt.plot(df['Volume Flow RateRMS'][500:].rolling(5).mean().values,label=path)
# plt.legend()
# print(np.diff(dfs[1].index))
order = 3
sm = from_pandas_dynamic(
    dfs[1:3], p=order
)

G = nx.Graph()
G.add_nodes_from(sm.nodes)
G.add_edges_from(sm.edges)

layout_func = nx.spring_layout

nt = Network(directed=True)
nt.repulsion()

init = [0, 0]
main_scale = [0, 600]
for i in range(order+1):
    filtered = ([node_l for node_l in sm.nodes if node_l.endswith(f"lag{i}")])
    filtered.remove(f"anomaly_lag{i}")
    nt.add_node(f"anomaly_lag{i}",
                x=init[0],
                y=init[1],
                physics=False)
    pos = layout_func(filtered, scale=200)
    for node in filtered:
        nt.add_node(node,
                    x=pos[node][0] + main_scale[0],
                    y=pos[node][1] + main_scale[1],
                    physics=False)
    init[0] += 600
    main_scale[0] += 600
    if i % 2 == 0:
        main_scale[1] = -600
    else:
        main_scale[1] = 600


# pos = nx.circular_layout(G, scale=1000)
# print(pos)
# for n in G.nodes:
#     nt.add_node(n,
#                 x=pos[n][0],
#                 y=pos[n][1],
#                 physics=False)
nt.add_edges(sm.edges)
for i in sm.edges:
    if 'Voltage_lag0' in i:
        print(i)
# nt.show('nx.html', notebook=False)
