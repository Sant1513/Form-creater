from embedding import VectorEmbeddings
import re

modules=[]
for i in range(1,6):
    file_path = f'DBMS/DBMS_MODULE_{i}'

# Open the file in read mode
    with open(file_path, 'r') as file:
    # Read the content of the file
        content = file.read()

    # Print the content
    #print(content)
        pattern = r"\d+\..*?\(\d{2} Marks"

# Find all matches
        questions = re.findall(pattern, content, re.DOTALL)

# Create a list to store the questions
        questions_list = []

# Add each matched question to the list
        for question in questions:
            questions_list.append(question.strip()[2:-9])
    modules.append(questions_list)

for i in modules:
    print(f"modules length:{len(i)}")

    #name should startand end with lowercase
subject="dbms1"
obj=VectorEmbeddings(modules,subject)
obj.embeddings()

# Print each question
    # for i, question in enumerate(questions_list, 1):
    #     print(f"Question {i}: {question}")

print(f"length is :{len(questions_list)}")

