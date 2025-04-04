import sys
import numpy as np
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from collections import defaultdict

def create_text_grid(words, grid_size=100):
    """
    Creates a grid representation of the text with spatial positioning
    grid_size: Number of vertical and horizontal divisions
    """
    if not words:
        return []
    
    # Get document boundaries
    x_coords = [w['x'] for w in words]
    y_coords = [w['y'] for w in words]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Initialize empty grid
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Calculate scaling factors
    x_scale = (max_x - min_x) / grid_size
    y_scale = (max_y - min_y) / grid_size
    
    # Place words in grid cells
    for word in words:
        # Calculate grid positions
        col = min(int((word['x'] - min_x) / x_scale), grid_size-1)
        row = min(int((word['y'] - min_y) / y_scale), grid_size-1)
        
        # Add word to grid cell
        if grid[row][col]:
            grid[row][col] += ' ' + word['text']
        else:
            grid[row][col] = word['text']
    
    return grid, (min_x, max_x, min_y, max_y)

def grid_to_text(grid, original_dimensions):
    """
    Converts the grid back to text while preserving spatial relationships
    """
    min_x, max_x, min_y, max_y = original_dimensions
    grid_rows, grid_cols = len(grid), len(grid[0])
    
    output_lines = []
    current_line = []
    prev_row_has_content = False
    
    for row in range(grid_rows):
        row_has_content = any(grid[row][col] for col in range(grid_cols))
        
        if row_has_content:
            # Process columns in this row
            line_parts = []
            for col in range(grid_cols):
                if grid[row][col]:
                    line_parts.append(grid[row][col])
            
            # Add line to output
            output_lines.append('  '.join(line_parts))  # Double space between columns
            
            prev_row_has_content = True
        elif prev_row_has_content:
            # Add empty line only if previous row had content
            output_lines.append('')
            prev_row_has_content = False
    
    return '\n'.join(output_lines)

def extract_pdf_structure(pdf_path, grid_size=100):
    """Extracts text while preserving original PDF structure using grid approach"""
    model = ocr_predictor(pretrained=True)
    pdf = DocumentFile.from_pdf(pdf_path)
    result = model(pdf)
    
    all_pages = []
    
    for page in result.export()['pages']:
        # Extract words with positions
        words = []
        for block in page['blocks']:
            for line in block['lines']:
                for word in line['words']:
                    words.append({
                        'text': word['value'],
                        'x': word['geometry'][0][0],
                        'y': word['geometry'][0][1],
                        'width': word['geometry'][1][0] - word['geometry'][0][0]
                    })
        
        # Create grid representation
        grid, dimensions = create_text_grid(words, grid_size)
        
        # Convert grid back to structured text
        page_text = grid_to_text(grid, dimensions)
        all_pages.append(page_text)
    
    return '\n\n'.join(all_pages)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python structured_extractor.py <document_name.pdf>')
        sys.exit(1)
    
    pdf_filename = sys.argv[1]
    extracted_text = extract_pdf_structure(pdf_filename)
    print(extracted_text)