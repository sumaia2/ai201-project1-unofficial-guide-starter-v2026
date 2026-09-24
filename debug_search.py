from store import search

results = search("What is the downside of living in Tamsin Court", top_k=20)
for r in results:
    print(r.label, round(r.distance, 3))
