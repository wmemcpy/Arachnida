import requests
from bs4 import BeautifulSoup
import os
import argparse
from urllib.parse import urljoin

def download_image(image_url, download_path):
	"""Downloads an image from a URL and saves it to the specified path."""
	try:
		response = requests.get(image_url, stream=True)
		response.raise_for_status()

		filename = os.path.basename(image_url)
		filepath = os.path.join(download_path, filename)

		with open(filepath, 'wb') as f:
			for chunk in response.iter_content(chunk_size=8192):
				f.write(chunk)
		print(f"Downloaded: {image_url} -> {filepath}")

	except requests.exceptions.RequestException as e:
		print(f"Error downloading {image_url}: {e}")
	except Exception as e:
		print(f"Error saving {image_url}: {e}")

def scrape_images(url, depth, max_depth, download_path):
	"""Recursively scrapes images from a URL."""
	if depth > max_depth:
		return

	try:
		response = requests.get(url)
		response.raise_for_status()

		soup = BeautifulSoup(response.text, 'html.parser')
		img_tags = soup.find_all('img')

		for img_tag in img_tags:
			src = img_tag.get('src')
			if src:
				absolute_url = urljoin(url, src)
				if any(absolute_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
					download_image(absolute_url, download_path)

		for a_tag in soup.find_all('a', href=True):
			link = a_tag['href']
			absolute_link = urljoin(url, link)
			scrape_images(absolute_link, depth + 1, max_depth, download_path)

	except requests.exceptions.RequestException as e:
		print(f"Error accessing {url}: {e}")
	except Exception as e:
		print(f"Error processing {url}: {e}")

def main():
	parser = argparse.ArgumentParser(description="Download images from a website recursively.")
	parser.add_argument("url", help="The URL to scrape.")
	parser.add_argument("-r", action="store_true", help="Enable recursive download.")
	parser.add_argument("-l", type=int, default=5, help="Maximum recursion depth (default: 5).")
	parser.add_argument("-p", default="./data/", help="Download directory (default: ./data/).")
	args = parser.parse_args()

	if not os.path.exists(args.p):
		os.makedirs(args.p)

	if args.r:
		scrape_images(args.url, 1, args.l, args.p)
	else:
		scrape_images(args.url, 1, 1, args.p)

if __name__ == "__main__":
	main()