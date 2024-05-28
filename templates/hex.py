input_string = "4xGhRSabz1"

# Initialize an empty string to store the hexadecimal representation
hex_string = ""

# Iterate through each character in the input string
for char in input_string:
    # Get the hexadecimal representation of the character
    hex_value = hex(ord(char)).lstrip("0x")
    hex_string += hex_value

# Print the hexadecimal representation
print(hex_string)
