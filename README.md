# Kumu Loop Discovery & Gap Analysis Tool

## 1. Background & Problem Statement

### **Background**

Systems thinking often involves using **Kumu** to map out complex causal relationships (Causal Loop Diagrams). In these maps, the most critical insights come from **feedback loops**—sequences of events that circle back to reinforce or balance a system.

### **The Problem**

As maps grow in complexity (e.g., analyzing *"How to solve the low participation rate in career institution activities?"*), it becomes humanly impossible to visually identify every single closed-circuit loop.

- **Hidden Dynamics:** Many critical feedback loops remain "hidden" because they weren't manually drawn or labeled in Kumu.
- **Audit Difficulty:** There is no native feature in Kumu to automatically list every mathematical cycle and compare it against the loops you have already named.

### **Importance**

Identifying these **"Unnamed Loops"** is vital for **Systemic Intervention**. If a loop exists but isn't named, you might miss a reinforcing engine that is driving the very problem you are trying to solve. This tool ensures 100% coverage of your system's logic.

## 2. Input, Output, and Impact

### **Input & Output**

| Feature | Description |
| :--- | :--- |
| **Input** | A `.json` file exported from a Kumu project (targeting the "Qualitative Map"). |
| **Output** | An `.xlsx` (Excel) file on your Desktop with "Unnamed" and "Named" loops listed. |

### **Expected Impact**

- **Completeness:** Automatically detects 100% of mathematical cycles using the `networkx` DFS-based algorithm.
- **Efficiency:** Saves hours of manual path-tracing by listing the full path of every hidden loop (e.g., `A -> B -> C -> A`).
- **Strategic Clarity:** Allows teams to systematically audit which loops are significant enough to be addressed in their strategy.

---

## 3. How It Works

The diagram below shows how the script processes your Kumu export from start to finish.

```
┌─────────────────────────────────────────────────────────────┐
│                        WORKFLOW                             │
│                                                             │
│  [Kumu Project]                                             │
│       │                                                     │
│       │  Export → JSON                                      │
│       ▼                                                     │
│  [kumu_export.json]                                         │
│       │                                                     │
│       │  Script reads nodes & connections                   │
│       ▼                                                     │
│  [NetworkX Directed Graph]                                  │
│       │                                                     │
│       ├──► DFS Cycle Detection (finds ALL closed loops)     │
│       │         │                                           │
│       │         ▼                                           │
│       │    [Full List of Mathematical Cycles]               │
│       │                                                     │
│       └──► Read existing Loop labels from JSON              │
│                 │                                           │
│                 ▼                                           │
│            [Named Loops List]                               │
│                                                             │
│  Gap Analysis: All Cycles vs. Named Loops                   │
│       │                                                     │
│       ├──► ✅ Named Loops   → Sheet 1                       │
│       └──► ⚠️  Unnamed Loops → Sheet 2                      │
│                                                             │
│  [loops_analysis.xlsx] saved to Desktop                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. How to Use

### **Prerequisites**

Ensure you have Python installed, then install the required libraries:

```bash
pip install networkx pandas openpyxl
```

### **Step-by-Step Instructions**

**Step 1 — Export from Kumu:**

1. Open your Kumu project.
2. Click the menu (bottom-left) → **Export** → **JSON**.
3. Save the file somewhere accessible (e.g., your Desktop or Downloads folder).

**Step 2 — Configure the Script:**

1. Open the `.py` script in any text editor or VS Code.
2. Locate the `=== 設定區 (Configuration) ===` section near the top.
3. Update `input_path` to the full path of your downloaded JSON file.

```python
# === 設定區 ===
input_path = "/Users/yourname/Desktop/kumu_export.json"   # ← update this
output_path = "/Users/yourname/Desktop/loops_analysis.xlsx"  # ← update if needed
```

**Step 3 — Run the Analysis:**

```bash
python your_script_name.py
```

**Step 4 — Review Results:**

1. Open `loops_analysis.xlsx` on your Desktop.
2. Navigate to the **"未命名閉環 (Unnamed Loops)"** sheet.
3. Each row shows a cycle path (e.g., `參與率低 → 活動吸引力不足 → 宣傳力道弱 → 參與率低`) that exists in your map but has **not** been labeled as a named loop in Kumu.
4. Use these findings to decide which loops deserve naming and strategic attention.

---

## 5. Output File Structure

The generated `loops_analysis.xlsx` contains two sheets:

| Sheet Name | Contents |
| :--- | :--- |
| **已命名閉環 (Named Loops)** | Loops that are already labeled in your Kumu map, with their full node path. |
| **未命名閉環 (Unnamed Loops)** | Loops detected by the algorithm that have **no** corresponding label in Kumu — your hidden dynamics. |

---

## 6. Interpreting the Results

Once you have your unnamed loops, consider asking:

- **Is this a Reinforcing (R) or Balancing (B) loop?**
  Reinforcing loops amplify change; balancing loops resist it.

- **Is this loop driving the core problem?**
  In a participation-rate analysis, a loop like `低參與 → 少資源 → 低品質活動 → 低參與` is a classic reinforcing trap.

- **Should this loop be named and added to your Kumu map?**
  If yes, add a Loop element in Kumu and label it (e.g., `R1: 惡性循環`). Re-run the script to confirm it moves from "Unnamed" to "Named."

---

## 7. Troubleshooting

| Issue | Solution |
| :--- | :--- |
| `ModuleNotFoundError` | Run `pip install networkx pandas openpyxl` again. |
| `FileNotFoundError` | Double-check the `input_path` in the script — ensure the path uses forward slashes or raw strings on Windows. |
| Output file not found | Check that `output_path` points to a directory you have write access to. |
| Zero unnamed loops found | All detected cycles are already named — great coverage! Or check that your Kumu JSON contains loop elements. |

---

## 8. License & Contribution

This tool is open for internal team use. If you find a bug or want to add features (e.g., loop polarity detection, HTML report output), feel free to open a pull request or reach out to the project maintainer.
