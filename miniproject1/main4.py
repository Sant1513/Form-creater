from langchain_community.llms import Ollama

# Initialize the LLaMA3 model using Ollama
llm = Ollama(model="llama3", temperature=0.06)

# Function to generate a poem
def generate_poem(text):
    prompt = '''take the below questions and generate the new question that matches the all three questions and it should be in 25 words
            
                '''+text
    poem = llm(prompt)
    return poem

if __name__ == "__main__":

    original_text = """Explain three Schema Architecture and reason for need of mapping among schema level? 
                        Describe three schema architecture. Explain characteristics of the Database approach? 
                        Explain three-schema architecture with a neat diagram. Why do we need mapping between schema levels?"""

    poem = generate_poem(original_text)
    print("STRUCTURED TEXT \n:", poem)
