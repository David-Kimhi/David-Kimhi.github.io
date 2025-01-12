# Boss Fight

## Overview

We have **N** warriors fighting a powerful boss. The boss has **unlimited health** and deals **B** units of damage per second. Each warrior **i** has:
- Health **H_i**
- Attack power **D_i** (damage per second)

However, **only two warriors** at a time will fight:
- Warrior **i** is on the front line, taking all of the boss’s damage until they are defeated.
- Warrior **j** is in the back line, attacking from the start of the fight until they are also defeated (after the front warrior falls).

Because the boss has unlimited health, the warriors cannot win. But they want to maximize the total damage dealt to the boss, meaning we look for the best pair of warriors **(i, j)** to yield the highest damage.

---

## Key Insight (Plain-Text Version)

### How Damage Accumulates

1. **Front warrior (i):**  
   - Time until defeated: health H_i over B (since boss deals B damage per second).  
   - Damage dealt by warrior i: D_i times (H_i over B).  

2. **Back warrior (j):**  
   - Starts attacking at second 0 and stops only when they themselves are defeated (which happens after i falls, and then j takes damage until H_j is depleted).  
   - Total time j is attacking: (H_i over B) plus (H_j over B).  
   - Damage dealt by warrior j: D_j times [(H_i over B) plus (H_j over B)].  

Therefore, total damage by the pair (i, j) is:
- D_i multiplied by (H_i over B)  
  plus  
- D_j multiplied by [ (H_i over B) plus (H_j over B) ].

We can also write that more compactly as:
D_i * H_i + D_j * (H_i + H_j),
all of which is then divided by B at the very end.

**Goal**: Find the maximum possible value of  
D_i * H_i + D_j * (H_i + H_j)  
for different i, j (with i not equal to j). Then divide that maximum by B.

---

## Why a Li Chao Tree?

A direct attempt to compute this for every pair (i, j) would be O(N^2), which can be too large when N is big. Instead, notice that for each warrior j, their contribution to total damage can be seen as:

- Slope = D_j  
- Intercept = D_j * H_j  

When we evaluate that line at x = H_i, we get D_j * H_i + D_j * H_j. This matches the back-warrior portion of our total damage.

A **Li Chao tree** is a data structure that maintains a set of lines (slope, intercept) and efficiently queries the maximum value at any point x. Here:
- We build the tree using each warrior j as a line of slope D_j and intercept D_j * H_j.
- Then, for each front warrior i (where x = H_i), we query the Li Chao tree for the best back warrior’s line value at that x.
- We add D_i * H_i (front warrior’s damage) to that query result.

### Handling i = j

We must ensure that, when querying with warrior i’s health H_i, we do not pick the **same** warrior j = i if that line happens to be the maximum. For that, the implementation keeps track of a **“second-best line”** at each node in the Li Chao tree, so if the best line corresponds to the same index i, we can fall back to the second-best line.

---

## Implementation Outline

1. **Line Class**  
   - Stores: slope (m), intercept (b), and the warrior index.  
   - Also keeps placeholders for “second-best line” in each segment of the tree.

2. **Building the Tree**  
   - Create a list (or array) of dummy lines for the tree structure.  
   - For each warrior j, insert a line with slope = D_j and intercept = D_j * H_j.

3. **Insertion** (insert function)  
   - Recursively decide which line is better over the current range.  
   - If the new line is better in part of the range, swap it in and push the old line to children.

4. **Query** (query function)  
   - Get the best line for a given x = H_i.  
   - If that best line’s index is the same as i, fall back to the second-best line.  
   - Return the maximum line value.

5. **Compute Final Answer**  
   - For each warrior i:
     - front_damage = D_i * H_i  
     - best_back_damage = query(H_i) (but skip i if i is the same index)  
     - total = front_damage + best_back_damage  
   - Track the maximum total across all i.  
   - Finally, divide that by B to get the damage.

