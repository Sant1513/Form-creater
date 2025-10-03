import chromadb
from chromadb.config import Settings
#from fetch_clustering import



class vector_DB:

    def __init__(self,vectors,module,subject,number):
        self.embeddings=vectors
        self.module=module
        self.subject=subject
        self.number=number
        #self.client = chromadb.Client(Settings(chromadb_path=r"C:/Users/varun/AppData/Roaming/Python/Python312/site-packages/chromadb"))
        #self.client=chromadb.Client()
        save_path=f"vectorDB/{self.subject}"
        self.client=chromadb.PersistentClient(path=save_path)
    
    def storing(self):
        collection_name = f"{self.subject}_module_{self.number}"
        collection = self.client.get_or_create_collection(name=collection_name)
        count=collection.count()
        sentences=[{"sentence": sentence} for sentence in self.module]

        ids=[str(id) for id in range(count,len(sentences)+count)]
        print(f"length of ids is{len(ids)}{count}")
        collection.add(
            #embeddings=self.embeddings.tolist(),
            embeddings=self.embeddings,
            metadatas=sentences,
            ids=ids
        )

        self.fetch_and_cluster(collection)


    def fetch_and_cluster(self,collection_name):

        # all_data = collection_name.fetch_all()
        results = collection_name.get(include=["embeddings", "metadatas"])
        print(f"fetching the embeddings of {self.subject}_module_{self.number}\n")
        #print("IDs:", results["ids"])
        #print("Documents:", results["documents"])

        #important
        # print("Embeddings:", results["embeddings"])
        # print("Metadatas:", results["metadatas"])
        print(len(results["embeddings"]))


        # for item in all_data:
        #     vector = item['embedding']
        #     metadata = item['metadata']
        #     print(f"Vector: {vector}, Metadata: {metadata}")

