import json
import networkx as nx
import pandas as pd
import os

# ================= 設定區 =================
# 把你的 JSON 檔案路徑貼在這裡
input_path = os.path.join(os.path.expanduser("~"), "Desktop", "kumu-boriswu-boriss-intern-mapping-如何解決職涯機構活動參與率低落的問題？-promotion-purpose (1).json")

# 輸出 Excel 存到桌面
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "loops_analysis.xlsx")

# 要分析哪一張地圖（通常是 'Qualitative Map'）
target_map_name = "Qualitative Map"
# ==========================================


def find_unnamed_loops():
    # 讀取檔案
    if not os.path.exists(input_path):
        print(f"❌ 找不到檔案：{input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Step 1: 找到目標地圖
    maps = data.get("maps", [])
    target_map = next((m for m in maps if m["name"] == target_map_name), None)
    if not target_map:
        print(f"❌ 找不到地圖：{target_map_name}")
        print(f"   現有地圖：{[m['name'] for m in maps]}")
        return

    # Step 2: 只抓地圖上用到的 element 和 connection IDs
    used_elem_ids = set(n["element"] for n in target_map["elements"])
    used_conn_ids = set(n["connection"] for n in target_map.get("connections", []))

    print(f"✅ 地圖上的 elements: {len(used_elem_ids)} 個")
    print(f"✅ 地圖上的 connections: {len(used_conn_ids)} 個")

    # Step 3: 建立 element ID → label 對應表
    id_to_label = {
        e["_id"]: e.get("attributes", {}).get("label", e["_id"])
        for e in data["elements"]
    }

    # Step 4: 只讀地圖上的 directed connections，建立圖
    conn_id_to_edge = {}
    map_edges = []
    for c in data["connections"]:
        if c["_id"] in used_conn_ids and c.get("direction") == "directed":
            frm = id_to_label.get(c["from"], c["from"])
            to = id_to_label.get(c["to"], c["to"])
            map_edges.append((frm, to))
            conn_id_to_edge[c["_id"]] = (frm, to)

    G = nx.DiGraph()
    G.add_edges_from(map_edges)

    # Step 5: 找出所有閉環
    print(f"\n🔄 正在運算閉環...")
    cycles = list(nx.simple_cycles(G))
    print(f"✅ 共找到 {len(cycles)} 個閉環")

    # Step 6: 讀取已命名的 loops（用 node set 比對）
    named_loops = data.get("loops", [])
    print(f"✅ Kumu 上已命名的 loop: {len(named_loops)} 個")

    named_nodesets = []
    for loop in named_loops:
        label = loop["attributes"].get("label", "?")
        nodes = set()
        for cid in loop["connections"]:
            edge = conn_id_to_edge.get(cid)
            if edge:
                nodes.add(edge[0])
                nodes.add(edge[1])
        named_nodesets.append({"label": label, "nodeset": frozenset(nodes)})

    # Step 7: 比對哪些閉環還沒被命名
    unnamed_rows = []
    named_rows = []

    for cycle in cycles:
        path = " -> ".join(cycle) + " -> " + cycle[0]
        cycle_nodes = frozenset(cycle)
        matched = [nl["label"] for nl in named_nodesets if nl["nodeset"] == cycle_nodes]

        if matched:
            named_rows.append({
                "現有名稱": " | ".join(matched),
                "Length": len(cycle),
                "Full Path": path,
            })
        else:
            unnamed_rows.append({
                "Loop ID": f"Unnamed_{len(unnamed_rows) + 1}",
                "Length": len(cycle),
                "Full Path": path,
            })

    print(f"\n{'='*40}")
    print(f"✅ 已命名閉環：{len(named_rows)} 個")
    print(f"⭐ 未命名閉環：{len(unnamed_rows)} 個（這些需要你去命名）")
    print(f"{'='*40}\n")

    # 印出未命名清單
    for row in unnamed_rows:
        print(f"{row['Loop ID']} (長度 {row['Length']}):")
        print(f"  {row['Full Path']}")
        print()

    # Step 8: 輸出 Excel
    with pd.ExcelWriter(output_path) as writer:
        pd.DataFrame(unnamed_rows).to_excel(writer, sheet_name="未命名閉環 (需命名)", index=False)
        pd.DataFrame(named_rows).to_excel(writer, sheet_name="已命名閉環", index=False)

    print(f"💾 Excel 已儲存至：{output_path}")


if __name__ == "__main__":
    find_unnamed_loops()