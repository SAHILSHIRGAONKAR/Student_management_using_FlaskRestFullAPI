import json

# Open the JSON file
with open('data.json', 'r') as file:
    # Load the JSON data
    data = json.load(file)

# Now you can work with the 'data' variable which contains the contents of the JSON file
# For example, you can print it
print(data)
