import pinecone
import sys
import os 

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_API_ENV'))

metadata_config = {
    "indexed": ["genre"]
}
#check if we already have an index, if not create it

hasIndex = pinecone.list_indexes()
#pinecone.delete_index(hasIndex[0])
print(hasIndex)
print(1)

if not hasIndex:
    pinecone.create_index("andrew-test", dimension=8, metadata_config=metadata_config, metric="cosine", pod_type="p1")
    print(2)
elif hasIndex[0] != "andrew-test":
    pinecone.delete_index(hasIndex[0])
    print(3)
    #we use dimension 1536 because thats what openai uses
    pinecone.create_index("andrew-test", dimension=8, metric="cosine", pod_type="p1")
    print(4)
else:
    index_name = hasIndex[0]
hasIndex = pinecone.list_indexes()

#store our index in this variable so we can interact with it
index = pinecone.Index("andrew-test")

#vector dbs use upserts to add new vectors
index.upsert([
    ("Andrew", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], {"genre": "comedy", "year": 2020}),
    ("Lulu", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], {"genre": "comedy", "year": 2021}),
    ("Love", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], {"genre": "comedy", "year": 2020}),
    ("Dog", [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4], {"genre": "comedy", "year": 1999}),
    ("Children", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], {"genre": "horror" })
], namespace="movies")
print(5)
index.upsert([
    ("Andrew", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
], namespace="movie_names")
print(6)

'''
Each query() request can contain only one of the parameters id or vector.
The vector should be the same length as the dimension of the index being queried. 

'''
# res = index.query(
#   vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
#   top_k=3,
#   include_values=True,
#   includeMetadata=True,
#   filter={"genre": { "$eq": "horror" }}
# )
# print(res)

# res = index.describe_index_stats(filter={"genre": { "$eq": "comedy" }})
# print(res)
res = index.query(
    vector=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    top_k=1,
    include_values=True,
    includeMetadata=True,
    filter={"genre": { "$eq": "comedy" }},
    namespace="movies"
)

print(res)

res = index.query(
    vector=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    top_k=1,
    namespace="movie_names"
)
print(res)
