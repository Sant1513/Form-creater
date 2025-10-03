from langchain_community.llms import Ollama

# Initialize the LLaMA3 model using Ollama
llm = Ollama(model="llama3", temperature=0)

# Function to generate a poem
def generate_poem():
    prompt = """write in a single question such that it matches contextual meaning of below questions
                 and use only termnologies which are present in the question as much as possible
                1) Define DBMS.Explain three schema architecture ?
                2) explain the uses of DBMS and Explain Three schema architecture?
                """
    poem = llm(prompt)
    print(poem)
generate_poem()
# if __name__ == "__main__":
#     pass
    
    #poem = generate_poem(original_text)
    #print("STRUCTURED TEXT \n:", poem)
