# Arachnida

Arachnida is a cybersecurity project consisting of two powerful image-related tools: Spider and Scorpion.

## Demo

<div align="center">
  <video width="640" height="480" controls>
    <source src="assets/example.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>

**Note:** If the video doesn't play directly in the README, you can [download the demo video](assets/example.mp4) to view it.

## Tools

### Spider (Web Crawler)

Spider is a command-line web crawler that downloads images from websites. It can recursively follow links to specified depths and save images to a local directory.

#### Features
- Download images from websites
- Support for common image formats (JPG, JPEG, PNG, GIF, BMP)
- Recursive crawling with configurable depth
- Customizable download directory

#### Usage
```bash
python spider.py [URL] [-r] [-l DEPTH] [-p PATH]
```

**Arguments:**
- `URL`: The website URL to crawl
- `-r`: Enable recursive download (follow links)
- `-l`: Maximum recursion depth (default: 5)
- `-p`: Download directory (default: ./data/)

**Example:**
```bash
# Download images from a website with recursion depth 2
python spider.py https://example.com -r -l 2 -p ./my_images/
```

### Scorpion (Metadata Analyzer)

Scorpion is a tool for viewing and manipulating metadata in image files. It can extract EXIF data and other metadata, with both command-line and GUI interfaces.

#### Features
- Extract image metadata including EXIF data
- View image properties (format, size, mode)
- Modify or delete metadata tags
- Interactive GUI for easy metadata visualization and editing
- Batch processing in command-line mode

#### Usage
```bash
python scorpion.py [FILES...] [-g]
```

**Arguments:**
- `FILES`: One or more image files to analyze (optional)
- `-g`: Force GUI mode even if files are provided

**Examples:**
```bash
# Command-line mode: display metadata for image.jpg
python scorpion.py image.jpg

# GUI mode: open file dialog to select images
python scorpion.py

# Force GUI mode with specific files
python scorpion.py image1.jpg image2.png -g
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Arachnida
```

2. Install the required dependencies:
```bash
pip install requests beautifulsoup4 pillow
```

## Requirements
- Python 3.6+
- requests
- beautifulsoup4
- PIL (Pillow)
- tkinter (included with most Python installations)

## Project Structure
```
Arachnida/
├── spider.py    # Web crawler for downloading images
├── scorpion.py  # Metadata extraction and manipulation tool
└── data/        # Default download directory
```

## Notes
- Spider will create the download directory if it doesn't exist
- Scorpion can display and edit various metadata formats
- Both tools have built-in error handling for common issues
- Scorpion will automatically fall back to command-line mode if it cannot connect to a display server
- For headless environments, use Scorpion without the `-g` flag to ensure command-line operation

## Troubleshooting

### Display Connection Issues
If you get an error like `_tkinter.TclError: couldn't connect to display ":0"`, Scorpion will automatically fall back to command-line mode. This typically happens in headless environments (servers without a GUI) or when X11 forwarding isn't properly set up.

Solutions:
1. Use Scorpion in pure command-line mode by providing file paths without the `-g` flag
2. Set up X11 forwarding if connecting via SSH
3. Use a VNC or remote desktop solution if GUI interaction is required
