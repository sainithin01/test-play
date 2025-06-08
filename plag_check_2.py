import os
from PIL import Image
from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from urllib.parse import unquote, urlparse


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class PlagiarismChecker:
    def __init__(self, threshold=0.5):
        # Download necessary NLTK resources
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        self.threshold = threshold
        
    def extract_text_from_image(self, image_path):
        """
        Extract text from an image using Tesseract OCR
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            str: Extracted text from the image
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Use Tesseract to do OCR on the image
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from {image_path}: {e}")
            return ""
    
    def preprocess_text(self, text):
        """
        Preprocess text by removing stopwords and converting to lowercase
        
        Args:
            text (str): Input text to preprocess
        
        Returns:
            str: Preprocessed text
        """
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        
        return ' '.join(filtered_tokens)
    
    def calculate_similarity(self, text1, text2):
        """
        Calculate similarity between two texts using SequenceMatcher
        
        Args:
            text1 (str): First text to compare
            text2 (str): Second text to compare
        
        Returns:
            float: Similarity score between 0 and 1
        """
        return SequenceMatcher(None, text1, text2).ratio()
    
    def search_internet(self, text, num_results=10):
        """
        Search the internet for similar content and return both links and their content.
        
        Args:
            text (str): Text to search for
            num_results (int): Number of search results to consider
        
        Returns:
            list: List of tuples containing (URL, page content)
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            query = '+'.join(text.split())
            url = f"https://www.google.com/search?q={query}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            links = [
                a['href'] for a in soup.find_all('a', href=True) 
                if "url?q=" in a['href']
            ]
            
            web_contents = []
            for link in links[:num_results]:
                try:
                    # Extract the actual URL
                    clean_url = link.split("&")[0].replace("/url?q=", "")
                    clean_url = unquote(clean_url)
                    parsed_url = urlparse(clean_url)
                    
                    # Check if the URL is valid
                    if parsed_url.scheme in ["http", "https"]:
                        page_response = requests.get(clean_url, headers=headers, timeout=5)
                        page_soup = BeautifulSoup(page_response.text, "html.parser")
                        content = page_soup.get_text()
                        web_contents.append((clean_url, content))
                except Exception as e:
                    print(f"Error fetching content from {link}: {e}")
            return web_contents
        except Exception as e:
            print(f"Error during web search: {e}")
            return []

    def check_plagiarism_from_internet(self, image_path):
        """
        Check plagiarism by searching for extracted text on the internet.
        """
        # Extract text from the source image
        source_text = self.extract_text_from_image(image_path)
        print(f"\nExtracted Text from Image:\n{source_text}\n")
        
        # Preprocess the extracted text
        processed_source_text = self.preprocess_text(source_text)
        
        # Search the internet for similar content
        print("Searching the internet for similar content...")
        web_results = self.search_internet(source_text)
        
        # Log the links being checked
        print("\nLinks Checked:")
        for i, (link, _) in enumerate(web_results, 1):
            print(f"Link {i}: {link}")
        
        # Compare source text with web contents
        plagiarism_results = {}
        for i, (link, web_content) in enumerate(web_results):
            similarity = self.calculate_similarity(processed_source_text, self.preprocess_text(web_content))
            plagiarism_results[link] = {
                'similarity': similarity,
                'is_plagiarized': similarity >= self.threshold
            }
        return plagiarism_results



def main():
    # Initialize plagiarism checker
    checker = PlagiarismChecker(threshold=0.5)
    
    print("Choose input type for plagiarism check:")
    print("1. Image")
    print("2. Text")
    print("3. Text File")
    choice = input("Enter your choice (1/2/3): ").strip()
    
    source_text = ""
    
    if choice == "1":
        # Image input
        source_image = input("Enter the path to the image: ").strip()
        source_text = checker.extract_text_from_image(source_image)
        print(f"\nExtracted Text from Image:\n{source_text}\n")
    elif choice == "2":
        # Text input
        source_text = input("Enter the text to check for plagiarism: ").strip()
    elif choice == "3":
        # Text file input
        text_file_path = input("Enter the path to the text file: ").strip()
        try:
            with open(text_file_path, 'r', encoding='utf-8') as file:
                source_text = file.read().strip()
            print(f"\nText from File:\n{source_text}\n")
        except Exception as e:
            print(f"Error reading text file: {e}")
            return
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Preprocess the extracted text
    print("Searching the internet for similar content...")
    web_results = checker.search_internet(source_text)
    
    # Log the links being checked
    print("\nLinks Checked:")
    for i, (link, _) in enumerate(web_results, 1):
        print(f"Link {i}: {link}")
    
    # Compare source text with web contents
    plagiarism_results = {}
    for i, (link, web_content) in enumerate(web_results):
        similarity = checker.calculate_similarity(checker.preprocess_text(source_text), checker.preprocess_text(web_content))
        plagiarism_results[link] = {
            'similarity': similarity,
            'is_plagiarized': similarity >= checker.threshold
        }
    
    # Print results
    print("\nPlagiarism Check Results:")
    for link, result in plagiarism_results.items():
        print(f"{link}:")
        print(f"Similarity: {result['similarity']:.2%}")
        print(f"Plagiarized: {result['is_plagiarized']}\n")

if __name__ == "__main__":
    main()
