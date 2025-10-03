from langchain_community.llms import Ollama
from PIL import Image

# Initialize the LLaMA model using Ollama
llm = Ollama(model="llama3", temperature=0.6)

# Function to convert image to text using LLaMA model
def image_to_text(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert image to a suitable format if needed (e.g., base64 encoding)
        # Assuming the LLaMA model can directly process image data
        img_data = img.tobytes()  # Example conversion, change as needed

        # Create a prompt for the LLaMA model to describe the image
        prompt = f"Describe the content of this image:\n{img_data}"
        
        # Get the response from the model
        response = llm(prompt)
        
        return response

if __name__ == "__main__":
    # Path to the image file
    image_path = "Screenshot 2024-07-05 132058.png"
    
    # Convert image to text
    text_output = image_to_text(image_path)
    
    # Print the output text
    print(text_output)
