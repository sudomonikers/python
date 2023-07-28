import pinecone
import os 

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_API_ENV'))

#check if we already have an index, if not create it
hasIndex = pinecone.list_indexes()
if hasIndex[0] != "andrew-test":
    pinecone.delete_index(hasIndex[0])
    #we use dimension 1536 because thats what openai uses
    pinecone.create_index("andrew-test", dimension=1536, metric="cosine", pod_type="p1")
else:
    index_name = hasIndex[0]

#store our index in this variable so we can interact with it
index = pinecone.Index("andrew-test")

#vector dbs use upserts to add new vectors
index.upsert([
    ("Andrew", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
    ("Lulu", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
    ("Love", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
    ("Dog", [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]),
    ("Children", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
])

res = index.describe_index_stats()
print(res)
'''
Each query() request can contain only one of the parameters id or vector.
The vector should be the same length as the dimension of the index being queried. 

'''
index.query(
  vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
  top_k=3,
  include_values=True,
  includeMetadata=True
)


#a good thing to do to find related examples is to query by id to get its vectos, then query by the vector to get similar vectors
queryres = index.query(
  id="Andrew",
  top_k=1,
  include_values=True,
  include_metadata=True
)
print(queryres)

newquery = index.query(
  vector=queryres.matches[0].values,
  top_k=2,
  include_metadata=True,
  include_values=True
)
#the following example shows how to filter by hardcoded
#filtered = list(filter(lambda x: x.id != "Andrew", newquery.matches))
filtered = list(filter(lambda x: x.id != queryres.matches[0].id, newquery.matches))
print(filtered)

#the following code deletes the index, however i am leaving it for testing purposes
#pinecone.delete_index("andrew-test")
