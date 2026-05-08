import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize
import matplotlib.cm as mcm

# -------------------------------------------------------------------
# 1.  Grid data
# -------------------------------------------------------------------
np.random.seed(42)
GRID_SIZE = 6
grid = np.random.randint(1, 20, size=(GRID_SIZE, GRID_SIZE))

# -------------------------------------------------------------------
# 2.  Core helper: cells hit by a line segment
# -------------------------------------------------------------------
def cells_under_arrow(start, end, grid_size, n_samples=800):
    sx, sy = start
    ex, ey = end
    hit = set()
    for t in np.linspace(0, 1, n_samples):
        col = int(np.floor(sx + t * (ex - sx)))
        row = int(np.floor(sy + t * (ey - sy)))
        if 0 <= row < grid_size and 0 <= col < grid_size:
            hit.add((row, col))

    def along_arrow(rc):
        r, c = rc
        cx, cy = c + 0.5, r + 0.5
        dx, dy = ex - sx, ey - sy
        L = np.hypot(dx, dy) or 1
        return ((cx - sx) * dx + (cy - sy) * dy) / L

    return sorted(hit, key=along_arrow)

def arrow_sum(start, end):
    cells = cells_under_arrow(start, end, GRID_SIZE)
    return sum(grid[r, c] for r, c in cells), cells

# -------------------------------------------------------------------
# 3.  Generate candidate arrows: all pairs of points on the 4 edges
#     Each edge is sampled at EDGE_SAMPLES positions.
# -------------------------------------------------------------------
EDGE_SAMPLES = 40   # increase for finer search (slower)
G = GRID_SIZE

def edge_points(n):
    """Sample n points along each of the 4 grid edges (in col, row coords)."""
    pts = []
    t = np.linspace(0.05, G - 0.05, n)
    for v in t:
        pts.append((0.0,  v))      # left edge
        pts.append((G + 0.0, v))   # right edge  (just outside)
        pts.append((v,  0.0))      # top edge
        pts.append((v,  G + 0.0))  # bottom edge
    return pts

candidates = edge_points(EDGE_SAMPLES)

MIN_CELLS = 4   # arrow must cross at least this many distinct cells

best_sum   = np.inf
best_start = None
best_end   = None
best_cells = None

for i, s in enumerate(candidates):
    for e in candidates[i+1:]:
        same_lr = (s[0] in (0.0, G+0.0)) and (e[0] in (0.0, G+0.0))
        same_tb = (s[1] in (0.0, G+0.0)) and (e[1] in (0.0, G+0.0))
        if same_lr or same_tb:
            continue
        total, cells = arrow_sum(s, e)
        if len(cells) < MIN_CELLS:
            continue
        if total < best_sum:
            best_sum   = total
            best_start = s
            best_end   = e
            best_cells = cells

print(f"Best arrow: {best_start} → {best_end}")
print(f"Cells hit:  {best_cells}")
print(f"Values:     {[grid[r,c] for r,c in best_cells]}")
print(f"Minimum sum: {best_sum}")

# -------------------------------------------------------------------
# 4.  Plot
# -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect("equal")
ax.set_xlim(0, GRID_SIZE)
ax.set_ylim(0, GRID_SIZE)
ax.invert_yaxis()

cmap = mcm.get_cmap("YlGnBu")
norm = Normalize(vmin=grid.min(), vmax=grid.max())
hit_set = set(best_cells)

for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        value  = grid[row, col]
        color  = cmap(norm(value))
        is_hit = (row, col) in hit_set

        rect = mpatches.FancyBboxPatch(
            (col + 0.04, row + 0.04), 0.92, 0.92,
            boxstyle="round,pad=0.02",
            linewidth=2.5 if is_hit else 0.8,
            edgecolor="#e05252" if is_hit else "#aaaaaa",
            facecolor=color, zorder=1,
        )
        ax.add_patch(rect)

        brightness = 0.299*color[0] + 0.587*color[1] + 0.114*color[2]
        txt_color  = "white" if brightness < 0.55 else "#222222"
        ax.text(col + 0.5, row + 0.5, str(value),
                ha="center", va="center",
                fontsize=14, fontweight="bold", color=txt_color, zorder=3)

# Red tint overlay on hit cells
for r, c in best_cells:
    ax.add_patch(mpatches.Rectangle(
        (c, r), 1, 1, linewidth=0, facecolor="#ff000018", zorder=2))

# Arrow — clamp endpoints to grid boundary for a clean look
sx, sy = np.clip(best_start[0], 0, G), np.clip(best_start[1], 0, G)
ex, ey = np.clip(best_end[0],   0, G), np.clip(best_end[1],   0, G)

ax.annotate("",
    xy=(ex, ey), xytext=(sx, sy),
    arrowprops=dict(
        arrowstyle="->,head_width=0.35,head_length=0.25",
        color="#cc1111", lw=3.5,
    ), zorder=5)

ax.set_title(f"Minimum-sum arrow  =  {best_sum}",
             fontsize=16, fontweight="bold", pad=14, color="#333333")
ax.text(0.01, 1.01,
        f"Cells: {best_cells}",
        transform=ax.transAxes, fontsize=8.5, color="#666666", va="bottom")

ax.axis("off")
plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/arrow_grid.png", dpi=150, bbox_inches="tight")
plt.show()
