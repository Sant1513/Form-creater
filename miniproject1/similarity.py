import chromadb
from chromadb.config import Settings
from sklearn.metrics.pairwise import cosine_similarity
import hdbscan
import numpy as np
from newquestions import generate_new
class similar:
    
    def __init__(self,subject):
        self.subject=subject
        #self.module_name=module_name
        save_path=f"vectorDB/{subject}"
        self.client=chromadb.PersistentClient(path=save_path)
        self.imp_questions=""
    def send_embeddings(self,module_name):
        collection_name = f"{self.subject}_module_{module_name}"
        collection = self.client.get_collection(name=collection_name)
        results = collection.get(include=["embeddings", "metadatas"])
        count=collection.count()
        # for i in range(count):
        #     print(f"{results["ids"][i]}. {results["metadatas"][i]["sentence"]}")
        len_embeddings=len(results["embeddings"])
        print(len_embeddings)
        #print(results["metadatas"])
        print("retrieved the embeddings successfully")

        return results["embeddings"]
    
    def retrieve(self,module_name):
        collection_name = f"{self.subject}_module_{module_name}"
        collection = self.client.get_collection(name=collection_name)
        results = collection.get(include=["embeddings", "metadatas"])
        count=collection.count()
        # for i in range(count):
        #     print(f"{results["ids"][i]}. {results["metadatas"][i]["sentence"]}")
        len_embeddings=len(results["embeddings"])
        print(len_embeddings)
        #print(results["metadatas"])
        print("retrieved the embeddings successfully")
        #
        #below line should include for using cosine similarity
        #
        # self.cosine_similar(results["embeddings"],len_embeddings,results["metadatas"],module_name)
        self.new_clustering_hdbscan(results["embeddings"],results["metadatas"],module_name)
    def cosine_similar(self,embeddings,leng,mod_sen,module_name):
        print(type(embeddings[0]))
        similarity_matrix = cosine_similarity(embeddings,embeddings)

        grouped_indices=set()
        cluster=[]
        for i in range(leng):
            each_dimen=[]
            for j in range(leng):
                if  similarity_matrix[i][j]>0.6 and similarity_matrix[i][j]<1 and j not in grouped_indices:
                    grouped_indices.add(j)
                    each_dimen.append(j)
            if len(each_dimen)>0:
                grouped_indices.add(i)
                each_dimen.append(i)
                cluster.append(each_dimen)
        print(cluster)
        self.imp_questions+=f"MODULE_{module_name}\n\n"
        for num,each_clus in enumerate(cluster):
            # print(f"{num+1}. {mod_sen[each_clus[0]]['sentence']}")
            self.imp_questions+=f"{num+1}. {mod_sen[each_clus[0]]['sentence']}"+"\n"

    def cosine_graph(self,embeddings,leng):
        similarity_matrix = cosine_similarity(embeddings, embeddings)
        grouped_indices = set()
        clusters = []
        cluster_labels = [-1] * leng  # Initialize all as noise

        for i in range(leng):
            if i not in grouped_indices:
                each_dimen = []
                for j in range(leng):
                    if 0.6 < similarity_matrix[i][j] < 1 and j not in grouped_indices:
                        grouped_indices.add(j)
                        each_dimen.append(j)
                if len(each_dimen) > 0:
                    grouped_indices.add(i)
                    each_dimen.append(i)
                    clusters.append(each_dimen)
                    cluster_id = len(clusters) - 1  # Assign cluster ID
                    for idx in each_dimen:
                        cluster_labels[idx] = cluster_id

        # Points not in any cluster remain labeled as -1 (noise)
        noise_points = [idx for idx, label in enumerate(cluster_labels) if label == -1]

        print(f"Clusters: {clusters}")
        print(f"Noise points: {noise_points}")
        return np.array(cluster_labels)
        
        

        # for each_clus in cluster:
        #     #print(mod_sen[each_clus[0]]['sentence'])
        #     print("cluster")
        #     for index in each_clus:
        #         print(mod_sen[index]['sentence'])
    def new_clustering_hdbscan(self,sentence_embedd,sentences,module_name):
        hdb = hdbscan.HDBSCAN(min_cluster_size=2)
        hdb.fit(sentence_embedd)
        labels=hdb.labels_
        clustered_sentences = {}
        print(labels)
        for sentence, label in zip(sentences, labels):
            if label not in clustered_sentences:
                clustered_sentences[label] = []
            clustered_sentences[label].append(sentence)

        #Print the clusters
        # for cluster, sentences_in_cluster in clustered_sentences.items():
        #     if cluster != -1:  # -1 is the label for outliers/noise
        #         print(f"\nCluster {cluster}:")
        #         for sentence in sentences_in_cluster:
        #             print(f" - {sentence}")
        #     else:
        #         print("\nOutliers (Noise):")
        #         for sentence in sentences_in_cluster:
        #             print(f" - {sentence}")

        clusters={}
        # new_obj=generate_new()
        set_labels=set(labels)
        list_lables=list(set_labels)
        list_lables.sort(key=lambda x : len(clustered_sentences[x]))

        for i in list_lables:
            if i!=-1:
                key=f"Cluster {i}"
                clusters[key]=clustered_sentences[i]
        if -1 in clustered_sentences:
            clusters["noise"] = clustered_sentences[-1]
        # for cluster, sentences_in_cluster in clustered_sentences.items():
        #     if cluster != -1:  # -1 is the label for outliers/noise
        #         key=f"Cluster {cluster}"
        #         # temp=[]
        #         # for sentence in sentences_in_cluster:
        #         #     temp.append(sentence)
        #         clusters[key]=sentences_in_cluster

        #     else:
        #         print("\nOutliers (Noise):")
        #         for sentence in sentences_in_cluster:
        #             print(f" - {sentence}")

        # print(clusters)
        # print(type(clusters["Cluster 0"][0]["sentence"]))
        
        #calling llm function
        llm_obj=generate_new(self.subject)
        llm_obj.llm_function(clusters,module_name)

        

                
    def append_in_file(self):
        self.subject="dbms2"#rewrite the subject name
        file_path=f"{self.subject}/imp_questions"
        with open(file_path, "w") as file:
            file.write(self.imp_questions)
        print("Successfully appended the important questions in the file")




if __name__=="__main__":
    subject="CO"
    #module_name="1"
    imp_ques=""
    obj=similar(subject)
    for i in range(1,6):
        # imp_ques+=f"MODULE_{i}"+'\n\n'
        obj.retrieve(str(i))
    # ncomment the below line for write in file
    #obj.append_in_file()
    
    
