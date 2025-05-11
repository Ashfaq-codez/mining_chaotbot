import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)

    text = ""
    # Iterate over all the pages in the PDF
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()  # Extract text from each page

    return text

def chunk_text(text, chunk_size=1000):
    # Split the text into chunks of approximately 'chunk_size' characters
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

# Example usage
if __name__ == "__main__":
    # Path to your PDF file
    pdf_path = "/Users/ashfaq/Desktop/amendment 2015.pdf"  # Full path to the PDF file

    # Extract text
    text = extract_text_from_pdf(pdf_path)

    # Chunk the extracted text into smaller pieces (e.g., 1000 characters each)
    chunks = chunk_text(text)

    # Print the first few chunks to verify
    for i, chunk in enumerate(chunks[:3]):  # Print first 3 chunks
        print(f"Chunk {i+1}: {chunk[:200]}...")  # Print a preview (first 200 characters) of each chunk

    # Optionally, save the chunks to a text file or JSON
    with open("MINES AND MINERALS (DEVELOPMENT AND REGULATION) ACT, 1957.txt", "w") as file:
        for chunk in chunks:
            file.write(chunk + "\n\n---\n\n")

    print("✅ Text chunking complete! Saved to 'MINES AND MINERALS (DEVELOPMENT AND REGULATION) ACT, 1957.txt'.")
