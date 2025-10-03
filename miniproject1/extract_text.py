import pytesseract
from pdf2image import convert_from_path
import os
import re
import shutil
from embedding import VectorEmbeddings
class basic_extracting:
    def __init__(self,subject):
        self.final_modules = []
        # self.subject="DBMS"
        self.subject=subject
        
    
    def extract_text_modulewise(self,pdf_path):
        # status='n'
        # while status=='n':
    # Convert PDF pages to images
        pages = convert_from_path(pdf_path, 300)  # The second argument is the DPI (dots per inch)

        extracted_text = ''
        for i, page in enumerate(pages):
    
            text = pytesseract.image_to_string(page)
            extracted_text += text + '\n'
        return extracted_text
        # Print or save the extracted text
        # print(extracted_text)
        # status=input('enter "n" for reexract or "y" for continue')
    def store_in_temp(self,text):
        with open("temporary", "w") as file:
            file.write(text)

        # print("check the temporary text file and edit manually if there is mistakes")
        # accept=input("click 'y' after the editing")
        # if accept=='y':
        self.fetch_text()
        
        # self.segment(extracted_text)
    def fetch_text(self):
        file_path="temporary"
        with open(file_path, 'r') as file:
        # Read the content of the file
            content = file.read()
        self.segment(content)


    def segment(self,extracted_text):
        lines = extracted_text.split('\n')
        module_1 = []
        module_2 = []
        module_3 = []
        module_4 = []
        module_5 = []
        current_module = []

        for line in lines:
            if 'Module-1' in line:
                current_module = module_1
            elif 'Module-2' in line:
                current_module = module_2
            elif 'Module-3' in line:
                current_module = module_3
            elif 'Module-4' in line:
                current_module = module_4
            elif 'Module-5' in line:
                current_module = module_5
            elif line.strip():
                current_module.append(line.strip())

        for i in [module_1,module_2,module_3,module_4,module_5]:
            self.final_modules.append(self.refine_text(i))
        obj=VectorEmbeddings(self.final_modules,self.subject)
        obj.embeddings()
        self.writing_text_file()
        print("writing into the respective modules are done")
    
    def writing_text_file(self):
        # Ask the user for the text they want to write
        
        question_text=''
        subject_folder=self.subject+"module_wise"
        # Define the file name
        #file_name = "paper.txt"

        if not os.path.exists(subject_folder):
            os.makedirs(subject_folder)

        for num,module in enumerate(self.final_modules):
            #question_text+=f"MODULE -{num}"+'\n'
            file_name=f"{subject_folder}_MODULE_{num+1}"
            question_text=''
            for questions in module:
                question_text+=questions+'\n'
            file_path = os.path.join(subject_folder, file_name)
            with open(file_path, "a") as file:
                file.write(question_text)

        # Open the file in write mode and write the user's text to it
        # with open(file_name, "w") as file:
        #     file.write(question_text)
        
        

         # Write question_text to file
        # file_path = os.path.join(dbms_folder, file_name)
        # with open(file_path, "w") as file:
        #     file.write(question_text)

        print(f"The text has been written to {file_name}")

        
        

    def refine_text(self,module):
        new_module=[]
        new_text='1. '
        counter=1
        pattern = re.compile(r'.*\d{2} Marks')
        for line in module:
            if line.strip()=='OR':
                continue
            elif pattern.match(line):
                new_text+=line+'\n'
                new_module.append(new_text)
                counter+=1
                new_text=f'{counter}. '
            else:
                new_text+=line+'\n'
        for i in range(len(new_module)):
            new_module[i]=new_module[i][2:-11] 
        return new_module
    #print(new_module)
    #print(module_1)

if __name__ == "__main__":
        # Path to the pdf file
    pdf_path=input("Enter the pdf_path")
    subject=input("Enter the subject name")
    # pdf_path = 'question_papers\DBMS question papers\June-2023- 18CS 53.pdf'
    extractor=basic_extracting(subject)
    extractor.extract_text_modulewise(pdf_path)
    print(len(extractor.final_modules))
        # Print the output text
        # for i in final_modules:
        #     for j in i:
        #         print(j)