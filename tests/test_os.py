import os
import logging

# Configure logging to print to console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to read the content of homepage.txt using current working directory
def load_homepage_text():
    try:
        # Get the current working directory and move up to the project root
        base_path = os.path.abspath(os.path.join(os.getcwd(), '..'))  # Go up one directory level
        logging.debug(f"Project root directory: {base_path}")
        
        # Construct the file path
        file_path = os.path.join(base_path, 'forms', 'homepage.txt')  # Adjust path
        logging.debug(f"Trying to open file: {file_path}")
        
        # Try to open the file
        with open(file_path, 'r') as file:
            content = file.read()
            logging.info(f"File Content: {content}")  # Log file content
            logging.info("File loaded successfully.")  # Confirm the file was loaded
        return content
    except FileNotFoundError:
        logging.error(f"Error: homepage.txt file not found at: {file_path}")
        return "This AI tool can be used to search the internet for useful advice on choosing appropriate research methods and gauging the ethical implications of these"
    except Exception as e:
        logging.exception(f"An error occurred while loading the file: {e}")
        return ""

if __name__ == "__main__":
    # Call the function and print/log the result
    logging.debug("Starting the test script.")
    load_homepage_text()
    logging.debug("Test script completed.")
