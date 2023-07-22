import pandas as pd
import numpy as np

articles = pd.read_csv("articles.csv")
sort = articles.sort_values(["total_events"])

output = sort[["url","title", "text", "lang", "total_events"]].head(20).values.tolist()
