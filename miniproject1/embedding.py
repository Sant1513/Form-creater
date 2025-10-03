from sentence_transformers import SentenceTransformer
from vector_db import vector_DB
class VectorEmbeddings:

    def __init__(self,modules,subject):
        self.subject=subject
        self.modules=modules
        self.vectors=[]
        self.model=SentenceTransformer('all-MiniLM-L6-v2')
    def embeddings(self):
        
        for name,module in enumerate(self.modules):
            module_embedding =self.model.encode(module)
            #self.vectors.append(module_embedding)
            #vector_obj=vector_DB(self.vectors,module,self.subject,name+1)
            print(f"length of each module_embedding is {len(module_embedding)}")
            vector_obj=vector_DB(module_embedding,module,self.subject,name+1)
            vector_obj.storing()
            #self.vectors=[]

        print("embeddings and storing them are done successfully")
        
        # sentences = ["Example sentence 1", "Example sentence 2"]

        # # Encode sentences
        # embeddings1 = self.model.encode(sentences)

        # # Print embeddings
        # for sentence, embedding in zip(sentences, embeddings1):
        #     print(f"Sentence: {sentence}")
        #     print(f"Embedding: {embedding}")
        #     print()

        
        
       
        
    
    
if __name__=="__main__":
    modules=[["what is your name","hi varun"],["varun bye"],["hye vamsi"],["bye vamsi"],["hi youth this is varun"]]
    temporary="temporary"
    #nmae is lower case
    # obj=VectorEmbeddings(modules,temporary)
    # obj.embeddings()