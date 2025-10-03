
from langchain_groq import ChatGroq
import os
class generate_new:

    def __init__(self,subject_name):
        self.llm = ChatGroq(
                                temperature=0,
                                model_name="llama-3.3-70b-versatile",
                                api_key="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"
                            )
        self.subject_name=subject_name
        

    def llm_function(self,clusters,module_name):
        print("in llm_function")
        # print(clusters)
        sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)
        print(f"module_{module_name}")
        imp_questions=f"module_{module_name}\n\n"
        additional_ques=""
        for cluster_name, sentences in sorted_clusters:
            # Combine the sentences into a single text
            combined_text = " ".join([s['sentence'] for s in sentences])

            # Formulate a query to extract combined important questions
            query = (f"From the following sentences: \"{combined_text}\", "
                    f"please combine overlapping and similar questions into a less number of concise set of important questions, "
                    f"without any explanations or additional text.")

            # Send the query to the Llama model
            response = self.llm.invoke(query)

            # Print only the important combined questions for each cluster
            #print(f"{cluster_name} - Important Combined Questions:")
            if cluster_name=="noise":
                additional_ques=response.content.strip()+"\n"
                continue
            imp_questions+=response.content.strip()+"\n"
            # print("")  # Using .strip() to clean up any leading/trailing whitespace
            # print("\n")
        imp_questions+="\n Additional Questions \n"+additional_ques+"\n"
        # print("\n"*5)
        subject_folder=self.subject_name+"module_wise"
        # Define the file name
        #file_name = "paper.txt"
        # print(imp_questions)
        if not os.path.exists(subject_folder):
            os.makedirs(subject_folder)
        file_name="important_questions"
        file_path = os.path.join(subject_folder, file_name)
        with open(file_path, "a") as file:
            file.write(imp_questions)


    