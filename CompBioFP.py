# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'CompBioFP/ASD meta abundance.csv'

data = pd.read_csv(file_path)

# Split the dataset into ASD (A-prefix columns) and Healthy (B-prefix columns)
asd_columns = [col for col in data.columns if col.startswith('A')]
healthy_columns = [col for col in data.columns if col.startswith('B')]

# Calculate the mean abundance for each taxonomy in both groups
data['ASD_mean'] = data[asd_columns].mean(axis=1)
data['Healthy_mean'] = data[healthy_columns].mean(axis=1)

# Compute the fold change (ASD vs Healthy)
data['Fold_Change'] = data['ASD_mean'] / data['Healthy_mean']
data['Fold_Change'] = data['Fold_Change'].replace([float('inf'), -float('inf')], float('nan'))

# Sort by the magnitude of fold change for meaningful patterns
filtered_data = data[['Taxonomy', 'ASD_mean', 'Healthy_mean', 'Fold_Change']].sort_values(by='Fold_Change', ascending=False)

# Filter top taxa with highest fold changes for visualization
top_taxa = filtered_data.head(20)

# Create a heatmap to show mean abundance in ASD vs Healthy
heatmap_data = top_taxa[['Taxonomy', 'ASD_mean', 'Healthy_mean']].set_index('Taxonomy')
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap='viridis', fmt=".2f", cbar_kws={'label': 'Mean Abundance'})
plt.title("Heatmap of Mean Taxa Abundance (ASD vs Healthy)")
plt.ylabel("Taxa")
plt.xlabel("Group")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot fold changes for top taxa
plt.figure(figsize=(12, 6))
sns.barplot(
    x="Fold_Change",
    y="Taxonomy",
    data=top_taxa.sort_values("Fold_Change", ascending=False),
    palette="coolwarm"
)
plt.title("Top Taxa by Fold Change (ASD / Healthy)")
plt.xlabel("Fold Change")
plt.ylabel("Taxa")
plt.tight_layout()
plt.show()