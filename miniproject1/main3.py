import chromadb

client = chromadb.Client()

# Get the collection you want to delete
collection = client.get_collection(name="dbms_module_1")

# Delete the collection
client.delete_collection(name="my_collection")