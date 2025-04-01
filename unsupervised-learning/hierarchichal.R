library(conflicted)
library(dplyr)
library(proxy)


df <- read.csv("text-mining-project-data/clean/lem-tfidf-100-samp.csv")

# Store the labels separately before removing them from the data frame
row_labels <- df$labels

# Remove the X and labels columns for distance calculation
no_lab <- df |> 
  select(-X, -labels)

dist_mat <- proxy::dist(no_lab, method="cosine")
groups_c <-hclust(dist_mat, method="ward.D")

# Use the labels for the dendrogram
plot(groups_c, cex=.7, hang=-30, main = "Cosine Sim", labels = row_labels)
rect.hclust(groups_c, k=5)

# Add cluster assignments to the original dataframe
# Cut the tree to get 5 clusters
cluster_assignments <- cutree(groups_c, k=5)

# Add the cluster labels as the first column of the dataframe
new_df <- cbind(cluster = cluster_assignments, df) |> 
  select(cluster, labels)

View(new_df)
