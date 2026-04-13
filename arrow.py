# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 20:29:40 2026

@author: sheng
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap

# -------------------------------------------------------------------
# 1.  Grid data
# -------------------------------------------------------------------
np.random.seed(0)
GRID_SIZE = 6
grid = np.random.randint(1, 5000, size=(GRID_SIZE, GRID_SIZE))

# -------------------------------------------------------------------
# 2.  Arrow definition  (start → end in grid col/row coordinates)
#     Origin is top-left: col increases right, row increases down.
# -------------------------------------------------------------------
arrow_start = (0.5, 0.5)   # (col, row) – cell centres, float allowed
arrow_end   = (4.8, 4.2)

# -------------------------------------------------------------------
# 3.  Find which cells the arrow passes through
#     Strategy: sample many points along the line segment and collect
#     unique (row, col) pairs that fall inside the grid.
# -------------------------------------------------------------------
def cells_under_arrow(start, end, grid_size, n_samples=500):
    """
    Return a list of (row, col) tuples for every grid cell whose centre
    is within half a cell-width of the arrow line segment, in traversal order.
    """
    sx, sy = start   # col, row
    ex, ey = end

    hit = set()
    for t in np.linspace(0, 1, n_samples):
        x = sx + t * (ex - sx)
        y = sy + t * (ey - sy)
        col = int(np.floor(x))
        row = int(np.floor(y))
        if 0 <= row < grid_size and 0 <= col < grid_size:
            hit.add((row, col))

    # Sort by position along the arrow direction for a clean printout
    def along_arrow(rc):
        r, c = rc
        cx, cy = c + 0.5, r + 0.5          # cell centre
        dx, dy = ex - sx, ey - sy
        length = np.hypot(dx, dy) or 1
        return ((cx - sx) * dx + (cy - sy) * dy) / length

    return sorted(hit, key=along_arrow)

hit_cells = cells_under_arrow(arrow_start, arrow_end, GRID_SIZE)
arrow_sum = sum(grid[r, c] for r, c in hit_cells)

# -------------------------------------------------------------------
# 4.  Plot
# -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect("equal")
ax.set_xlim(0, GRID_SIZE)
ax.set_ylim(0, GRID_SIZE)
ax.invert_yaxis()          # row 0 at top, matches array indexing

cmap = get_cmap("YlGnBu")
norm = Normalize(vmin=grid.min(), vmax=grid.max())

for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        value   = grid[row, col]
        color   = cmap(norm(value))
        is_hit  = (row, col) in hit_cells

        rect = mpatches.FancyBboxPatch(
            (col + 0.04, row + 0.04),
            0.92, 0.92,
            boxstyle="round,pad=0.02",
            linewidth=2.5 if is_hit else 0.8,
            edgecolor="#e05252" if is_hit else "#aaaaaa",
            facecolor=color,
            zorder=1,
        )
        ax.add_patch(rect)

        # Cell value label
        brightness = 0.299*color[0] + 0.587*color[1] + 0.114*color[2]
        txt_color  = "white" if brightness < 0.55 else "#222222"
        ax.text(
            col + 0.5, row + 0.5, str(value),
            ha="center", va="center",
            fontsize=14, fontweight="bold", color=txt_color,
            zorder=3,
        )

# --- Arrow (in data-coords: x=col, y=row) ---------------------------
ax.annotate(
    "",
    xy=(arrow_end[0], arrow_end[1]),
    xytext=(arrow_start[0], arrow_start[1]),
    arrowprops=dict(
        arrowstyle="->,head_width=0.35,head_length=0.25",
        color="#cc1111",
        lw=3.5,
        connectionstyle="arc3,rad=0.0",
    ),
    zorder=5,
)

# --- Highlight hit cells with a subtle red tint overlay -------------
for row, col in hit_cells:
    ax.add_patch(mpatches.Rectangle(
        (col, row), 1, 1,
        linewidth=0, facecolor="#ff000018", zorder=2,
    ))

# --- Title & annotation ---------------------------------------------
ax.set_title(
    f"Arrow sum  =  {arrow_sum}",
    fontsize=16, fontweight="bold", pad=14,
    color="#333333",
)
ax.text(
    0.01, 1.01,
    f"Cells crossed: {[(r,c) for r,c in hit_cells]}",
    transform=ax.transAxes,
    fontsize=8.5, color="#666666",
    va="bottom",
)

ax.axis("off")
plt.tight_layout()
plt.savefig("arrow_grid.png", dpi=150, bbox_inches="tight")
plt.show()

# --- Console summary ------------------------------------------------
print("Grid:")
print(grid)
print(f"\nArrow from col/row {arrow_start} → {arrow_end}")
print(f"Cells hit (row, col): {hit_cells}")
print(f"Values: {[grid[r,c] for r,c in hit_cells]}")
print(f"Sum: {arrow_sum}")