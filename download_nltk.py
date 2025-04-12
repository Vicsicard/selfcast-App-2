"""Download required NLTK data."""
import nltk

def main():
    """Download required NLTK data packages."""
    required_packages = [
        'punkt',              # For sentence tokenization
        'averaged_perceptron_tagger',  # For POS tagging
        'stopwords',          # For stopwords
        'wordnet',           # For word meanings
        'vader_lexicon'      # For sentiment analysis
    ]
    
    for package in required_packages:
        print(f"Downloading {package}...")
        nltk.download(package)
        print(f"Downloaded {package}")

if __name__ == "__main__":
    main()
