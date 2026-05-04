---
name: Training Accuracy Visualization Design
description: Design for visualizing training accuracy over batches and epochs from parsed log CSV files
type: design
date: 2026-05-04
---

# Training Accuracy Visualization Design

## Overview

Create a Jupyter notebook (`analysis.ipynb`) that automatically discovers parsed training log CSVs, generates accuracy-over-time visualizations showing epoch boundaries, and saves plots both inline and to files.

## Context

- Project: Vehicle re-identification coursework (EEEM071)
- Training logs have been parsed into CSV files in `results/` directory
- Each experiment has a `{experiment_name}_training.csv` file
- CSV structure includes columns: `epoch`, `batch`, `total_batches`, `acc_instant`, `acc_avg`, and various loss/time metrics
- Currently 7 experiments parsed (googlenet variants, resnet50, mobilenet_v3_small, vgg16)

## Requirements

1. **Auto-discovery**: Find all training CSV files in `results/` directory
2. **Visualization**: Plot average accuracy (`acc_avg`) over batch progression
3. **Epoch markers**: Show where each epoch begins with vertical lines and labels
4. **Output**: Display plots inline in notebook AND save to `figures/` directory as PNG files
5. **Separate plots**: One plot per experiment (not combined)

## Architecture

### Component 1: Data Discovery and Loading

**Purpose**: Find and load all training CSVs

**Implementation**:
- Use `pathlib.Path` or `glob` to find files matching `results/*_training.csv`
- Extract experiment name from filename by removing `_training.csv` suffix
- Load each CSV with `pandas.read_csv()`
- Return list of tuples: `(experiment_name, dataframe)`

**Data structure**:
```python
experiments = [
    ("googlenet-veri", DataFrame),
    ("resnet50-veri", DataFrame),
    ...
]
```

### Component 2: Epoch Boundary Detection

**Purpose**: Identify where epochs change for drawing vertical lines

**Implementation**:
- Use pandas to detect where `epoch` column value increases
- Return list of indices where new epochs start
- Extract epoch numbers for labeling

**Example logic**:
```python
epoch_changes = df['epoch'].ne(df['epoch'].shift())
epoch_boundaries = df[epoch_changes].index.tolist()
```

### Component 3: Plotting Function

**Purpose**: Create individual accuracy plot for one experiment

**Function signature**: `plot_accuracy(experiment_name, df, save_dir='figures/')`

**Implementation**:
- Create matplotlib figure (size: 12x6 inches)
- Plot `acc_avg` against sequential row index
- Add vertical lines at epoch boundaries using `axvline()`
- Label epoch boundaries with text annotations
- Configure:
  - Title: experiment name (cleaned up for readability)
  - X-axis label: "Batch"
  - Y-axis label: "Average Accuracy (%)"
  - Grid: enabled for readability
  - Line color: solid line, reasonable thickness
- Display with `plt.show()`
- Save to `{save_dir}/{experiment_name}_accuracy.png` at 300 DPI

**Epoch boundary styling**:
- Vertical lines: dashed, gray, alpha=0.7
- Text labels: "Epoch N" positioned near top of plot

### Component 4: Output Directory Management

**Purpose**: Ensure output directory exists

**Implementation**:
- Check if `figures/` directory exists
- Create it if missing using `os.makedirs(exist_ok=True)`

### Component 5: Main Workflow

**Purpose**: Orchestrate the entire process

**Implementation sequence**:
1. Create output directory
2. Discover all training CSVs
3. For each experiment:
   - Load CSV
   - Generate plot (displays inline + saves to file)
4. Print summary: number of plots generated and output location

## Data Flow

```
results/*.csv → Data Discovery → Load DataFrames → 
For each experiment:
  → Detect Epoch Boundaries → 
  → Create Plot → 
  → Display Inline (plt.show()) → 
  → Save to figures/*.png
```

## File Structure

```
Surrey_EEEM071_Coursework/
├── results/
│   ├── googlenet-veri_training.csv
│   ├── resnet50-veri_training.csv
│   └── ...
├── figures/                          # Created by script
│   ├── googlenet-veri_accuracy.png
│   ├── resnet50-veri_accuracy.png
│   └── ...
└── analysis.ipynb                    # Implementation location
```

## Implementation Notes

### Libraries Required
- `pandas`: CSV loading and data manipulation
- `matplotlib.pyplot`: Plotting
- `pathlib` or `glob`: File discovery
- `os`: Directory creation

### Error Handling
- Handle case where `results/` directory doesn't exist
- Handle case where no CSV files are found
- Skip files that fail to load (print warning)

### Plot Styling Considerations
- Use default matplotlib style (clean, professional)
- Ensure epoch labels don't overlap (offset if needed)
- Y-axis should show percentage values clearly
- X-axis should show batch numbers as integers

### Performance
- For 7 experiments with ~590 batches × 10 epochs each (~5900 points), performance is not a concern
- No need for downsampling or optimization

## Success Criteria

1. ✓ All training CSVs in `results/` are automatically discovered
2. ✓ Each experiment generates one plot showing accuracy progression
3. ✓ Epoch boundaries are clearly marked with vertical lines and labels
4. ✓ Plots display inline in notebook
5. ✓ Plots save to `figures/` directory as PNG files
6. ✓ Code is contained in `analysis.ipynb` notebook
7. ✓ Process is repeatable (can re-run to regenerate plots)

## Future Enhancements (Out of Scope)

- Comparing multiple experiments on same plot
- Interactive plots with plotly
- Additional metrics (loss, instant accuracy)
- Statistical analysis of training curves
- Automatic detection of overfitting or training issues
