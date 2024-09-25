import re
from bs4 import BeautifulSoup

# Regular expressions to match non-breaking space (&nbsp;) and zero-width space (ninja space)
nbsp_pattern = re.compile(r'&nbsp;')
ninja_space_pattern = re.compile(r'[\u200B-\u200D]')  # Matches zero-width space (U+200B to U+200D)

# Function to clean up aria-label, meta description, and visually hidden elements
def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Clean aria-label attributes
    for element in soup.find_all(attrs={"aria-label": True}):
        cleaned_label = re.sub(nbsp_pattern, ' ', element['aria-label'])  # Replace &nbsp; with space
        cleaned_label = re.sub(ninja_space_pattern, '', cleaned_label)    # Remove ninja spaces
        element['aria-label'] = cleaned_label

    # Clean meta descriptions
    for meta in soup.find_all('meta', attrs={"name": "description"}):
        if 'content' in meta.attrs:
            cleaned_content = re.sub(nbsp_pattern, ' ', meta['content'])
            cleaned_content = re.sub(ninja_space_pattern, '', cleaned_content)
            meta['content'] = cleaned_content

    # Clean visually hidden elements (e.g., using class 'visually-hidden', 'sr-only', etc.)
    for element in soup.find_all(class_=re.compile(r'(visually-hidden|sr-only|hidden)')):
        cleaned_text = re.sub(nbsp_pattern, ' ', element.get_text())
        cleaned_text = re.sub(ninja_space_pattern, '', cleaned_text)
        element.string = cleaned_text

    return str(soup)

# Function to load HTML from file, clean it, and save it back to the file
def clean_html_file(input_file, output_file):
    # Open and read the external HTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Clean the HTML content
    cleaned_html = clean_html(html_content)

    # Write the cleaned HTML back to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)

    print(f"Cleaned HTML has been saved to {output_file}")

# Sample usage
if __name__ == "__main__":
    # Input HTML file path and output file path
    input_html_file = 'input.html'   # Replace with your input HTML file
    output_html_file = 'output.html' # Replace with your desired output HTML file

    # Clean the HTML file
    clean_html_file(input_html_file, output_html_file)