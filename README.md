# Experiments with Vector Databases
Learning how to use Vector Databases to do cool things.

## Analogies

Converts words into Vectors allowing us to add and subtract other words to get conceptually similar analgous words.

### Examples:

```
actor - man + woman = ?

Most similar words:
actress: 0.8764
actresses: 0.6629


France - Paris + Rome = ?

Most similar words:
Italy: 0.7115
Sicily: 0.5600
Italians: 0.5600
```

## Summarize Star Wars Collecting

Answer questions about Star Wars Collecting by using a custom Vector Database using my personal knowledge store.

- Parse my collecting information books in pdf format into Markdown
- Chunk markdown files into ChromaDb 
- Query ChromaDb to fetch matching documents
- (TODO) use small LLM to summarize returned documents
