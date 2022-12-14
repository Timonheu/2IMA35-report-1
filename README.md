# Discovering Parties in House of Representatives using Affinity Clustering

This code is part of the first group assignment of the TU/e course 2IMA35 - Massively Parallel Algorithms. This code pulls information from twitter, namely who follows who, and uses that information to construct an undirected weighted graph. It then attempts to use affinity clustering to rediscover existing relations between the twitter users. In our case, we attempted to rediscover the parties of the Dutch house of representatives everybody belonged to.

This code heavily uses code by Kees Voorintholt: https://github.com/Keesiev7/MSTforDenseGraphs. This code is found in the folder "Code Kees".

Python: 3.6.0 <br />
Pyspark: 3.0.2 <br />
matplotlib: 3.3.4 <br />
