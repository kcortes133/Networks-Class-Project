# Evaluating the Contributions of Model Organisms to the MonarchKG

## Goal:
Determine how different model organisms contribute to the Monarch KG and influence predictions
for novel gene-disease relationships.

## Description:
This program takes a version of MonarchKG and outputs information about the model organism node and 
edge connections, connectivity and types related to each other and human disease. 

It also runs a pipeline to assess how each model organism contributes to embeddings and predictions about
human disease using the MonarchKG. It individually removes each model organism and associated edges,
then removes a random subset of the remaining edges. This random subset is also removed from the unedited Monarch KG
both the edited and unedited Monarch KG are then embedded and the random subset of removed edges is predicted. We then calculate 
how many of the removed edges were able to be repredicted without a model organism in the graph.

