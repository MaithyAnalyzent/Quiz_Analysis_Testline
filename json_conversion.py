import json

def convert_to_structured_json(input_file_path, output_file_path):
    """
    Converts an unstructured JSON file to a structured JSON file.

    Args:
        input_file_path (str): Path to the input JSON file.
        output_file_path (str): Path to save the structured JSON file.
    """
    try:
        # Load the content of the input file
        with open(input_file_path, 'r') as input_file:
            data = json.load(input_file)

        # Structure the data
        structured_data = {"quiz_attempts": data}

        # Save the structured data to the output file
        with open(output_file_path, 'w') as output_file:
            json.dump(structured_data, output_file, indent=4)

        print(f"Structured JSON file saved at: {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Input and output file paths
input_file_path = "Quiz_Endpoint1.json"  # Replace with your input file path
output_file_path = "Structured_Quiz_Attempts.json"  # Replace with your desired output file path

# Call the function to convert and structure the JSON
convert_to_structured_json(input_file_path, output_file_path)
