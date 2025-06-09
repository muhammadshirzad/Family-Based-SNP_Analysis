# 🛠️ Step 1: Install required packages
!pip install networkx matplotlib pandas openpyxl

# 📚 Step 2: Import packages
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from google.colab import files

# 📤 Step 3: Upload your Excel file
print("📤 Upload your pedigree Excel file...")
uploaded = files.upload()
filename = list(uploaded.keys())[0]

# 📄 Step 4: Load and filter for Family 
df = pd.read_excel(filename)
df = df[df["FID"] == ?]  # Filter Family ? only
df = df.astype(str)       # Ensure IDs are treated as strings

# 👨‍👩‍👧 Step 5: Create edge list
edges = []
for _, row in df.iterrows():
    if row["PAT"] != '0':
        edges.append((row["PAT"], row["IID"]))
    if row["MAT"] != '0':
        edges.append((row["MAT"], row["IID"]))

# 📈 Step 6: Build graph
G = nx.DiGraph()
G.add_edges_from(edges)

# 🎨 Step 7: Radial layout plot
plt.figure(figsize=(10, 14))
nx.draw(G, pos=nx.circular_layout(G), with_labels=True, node_color='lightblue',
        node_size=3000, edge_color='gray', font_size=10, font_weight='bold')
plt.title("Radial Pedigree Layout (Family 36)")
plt.axis('off')
plt.show()

# 🔄 Step 8: U-shaped layout (safe shell layout with fallback)
gen0 = set(df[(df["PAT"] == "0") & (df["MAT"] == "0")]["IID"])
gen1 = set(df[(df["PAT"].isin(gen0)) | (df["MAT"].isin(gen0))]["IID"])
gen2 = set(df[~df["IID"].isin(gen0.union(gen1))]["IID"])

# ✅ Combine all node IDs from graph to avoid KeyError
all_ids = set(G.nodes)
assigned_ids = gen0.union(gen1).union(gen2)
unassigned = all_ids - assigned_ids

# Add unassigned nodes to the last shell
shells = [list(gen0), list(gen1), list(gen2.union(unassigned))]

# 🔁 Generate layout
pos_shell = nx.shell_layout(G, shells)

# 📊 Plot
plt.figure(figsize=(10, 14))
nx.draw(G, pos_shell, with_labels=True, node_color='lightblue', node_size=3000,
        edge_color='gray', font_size=10, font_weight='bold')
plt.title("U-Shaped Pedigree Layout (Family 36)")
plt.axis('off')
plt.show()
