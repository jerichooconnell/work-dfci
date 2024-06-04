# Read the root file modules.root using uproot and print information about the file and it's contents.
#

import uproot

# Open the file using uproot
file = uproot.open("modules.root")

# Print the file information
print(file)

# Print the keys in the file
print(file.keys())

# # Print the keys in the file
# print(file["modules"].keys())

# # Print the keys in the file
# print(file["modules"]["module1"].keys())
