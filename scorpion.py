import argparse
import os
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def get_metadata(image_path):
	"""Extracts metadata from an image file, returning a dictionary."""
	metadata = {}
	try:
		img = Image.open(image_path)
		metadata["File"] = image_path
		metadata["Format"] = img.format
		metadata["Size"] = img.size
		metadata["Mode"] = img.mode

		if hasattr(img, '_getexif') and img._getexif() is not None:
			exif_data = img._getexif()
			metadata["EXIF"] = {}
			for tag_id, value in exif_data.items():
				tag = TAGS.get(tag_id, tag_id)
				metadata["EXIF"][tag] = value

	except (FileNotFoundError, OSError, ValueError) as e:
		messagebox.showerror("Error", f"Could not open or read image: {e}")
		return None
	except Exception as e:
		messagebox.showerror("Error", f"An unexpected error occurred: {e}")
		return None
	return metadata

def modify_metadata(image_path, metadata):
	"""Modifies the metadata of an image file."""
	try:
		img = Image.open(image_path)
		if "EXIF" in metadata:
			exif_data = img.getexif()
			for tag, value in metadata["EXIF"].items():
				tag_id = None
				for k, v in TAGS.items():
					if v == tag:
						tag_id = k
						break
				if tag_id is not None:
					if value is None:
						if tag_id in exif_data:
							del exif_data[tag_id]
					else:
						exif_data[tag_id] = value
				else:
					print(f"Warning, unknown Tag: {tag}")

			img.save(image_path, "jpeg", exif=exif_data.tobytes())
			messagebox.showinfo("Success", "Metadata modified successfully.")
		else:
			img.save(image_path, "jpeg")
			messagebox.showinfo("Success", "Image saved (no EXIF changes).")


	except (FileNotFoundError, OSError, ValueError) as e:
		messagebox.showerror("Error", f"Could not modify image: {e}")
	except Exception as e:
		messagebox.showerror("Error", f"An unexpected error occurred during modification: {e}")

def display_metadata_gui(metadata):
	"""Displays metadata in a Tkinter window and allows modification."""
	if not metadata:
		return

	window = tk.Toplevel()
	window.title("Metadata Viewer/Editor")

	# Display basic info
	basic_frame = tk.Frame(window)
	basic_frame.pack(padx=10, pady=5)
	tk.Label(basic_frame, text=f"File: {metadata.get('File', 'N/A')}").pack()
	tk.Label(basic_frame, text=f"Format: {metadata.get('Format', 'N/A')}").pack()
	tk.Label(basic_frame, text=f"Size: {metadata.get('Size', 'N/A')}").pack()
	tk.Label(basic_frame, text=f"Mode: {metadata.get('Mode', 'N/A')}").pack()

	# Display and edit EXIF data (if present)
	if "EXIF" in metadata:
		exif_frame = tk.Frame(window)
		exif_frame.pack(padx=10, pady=5)
		tk.Label(exif_frame, text="EXIF Data:").pack()

		for tag, value in metadata["EXIF"].items():
			tag_frame = tk.Frame(exif_frame)
			tag_frame.pack(fill=tk.X)
			tk.Label(tag_frame, text=f"{tag}: ", width=20, anchor='w').pack(side=tk.LEFT)
			value_label = tk.Label(tag_frame, text=str(value), wraplength=300, anchor='w')
			value_label.pack(side=tk.LEFT)

			def edit_tag(t=tag, v=value, meta=metadata):
				new_value = simpledialog.askstring("Edit Metadata", f"Enter new value for {t}:", initialvalue=str(v))
				if new_value is not None:
					meta["EXIF"][t] = new_value
					value_label.config(text=new_value)
			def delete_tag(t=tag, meta=metadata):
				if messagebox.askyesno("Delete Tag", f"Are you sure to delete {t}?"):
					meta["EXIF"][t] = None
					tag_frame.destroy()

			edit_button = tk.Button(tag_frame, text="Edit", command=edit_tag)
			edit_button.pack(side=tk.LEFT)

			delete_button = tk.Button(tag_frame, text="Delete", command=delete_tag)
			delete_button.pack(side=tk.LEFT)

	# Save button
	def save_changes():
		modify_metadata(metadata["File"], metadata)
		window.destroy()

	save_button = tk.Button(window, text="Save Changes", command=save_changes)
	save_button.pack(pady=10)

	# Display image (optional)
	try:
		img = Image.open(metadata['File'])
		img.thumbnail((300, 300))
		photo = ImageTk.PhotoImage(img)
		image_label = tk.Label(window, image=photo)
		image_label.image = photo
		image_label.pack()
	except:
		pass

def open_file_dialog():
	"""Opens a file dialog and displays metadata for selected images."""
	filepaths = filedialog.askopenfilenames(
		title="Select Image Files",
		filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"), ("All files", "*.*")]
	)
	for filepath in filepaths:
		metadata = get_metadata(filepath)
		if metadata:
			display_metadata_gui(metadata)


def main():
	parser = argparse.ArgumentParser(description="Extract and modify metadata from image files.")
	parser.add_argument("files", nargs="*", help="One or more image files.  If none, opens file dialog.")
	parser.add_argument("-g", "--gui", action="store_true", help="Use GUI even if files are provided.")
	args = parser.parse_args()

	if args.files and not args.gui:
		# Command-line mode
		for file_path in args.files:
			metadata = get_metadata(file_path)
			if metadata:
				print(f"File: {metadata.get('File', 'N/A')}")
				print(f"  Format: {metadata.get('Format', 'N/A')}")
				print(f"  Size: {metadata.get('Size', 'N/A')}")
				print(f"  Mode: {metadata.get('Mode', 'N/A')}")
				if 'EXIF' in metadata:
					print('  EXIF data:')
					for tag, value in metadata['EXIF'].items():
						print(f'   {tag}: {value}')
				else:
					print('   No EXIF data found.')
	else:
		# GUI mode with fallback to command-line
		try:
			root = tk.Tk()
			root.title("Scorpion - Image Metadata Tool")
			
			if args.files:
				for file_path in args.files:
					metadata = get_metadata(file_path)
					if metadata:
						display_metadata_gui(metadata)
			else:
				open_button = tk.Button(root, text="Open Image(s)", command=open_file_dialog)
				open_button.pack(pady=20)
			
			root.mainloop()
		except tk.TclError as e:
			print(f"ERROR: Cannot open GUI display: {e}")
			print("Falling back to command-line mode.")
			
			# Fall back to command-line mode if GUI fails
			if args.files:
				for file_path in args.files:
					metadata = get_metadata(file_path)
					if metadata:
						print(f"File: {metadata.get('File', 'N/A')}")
						print(f"  Format: {metadata.get('Format', 'N/A')}")
						print(f"  Size: {metadata.get('Size', 'N/A')}")
						print(f"  Mode: {metadata.get('Mode', 'N/A')}")
						if 'EXIF' in metadata:
							print('  EXIF data:')
							for tag, value in metadata['EXIF'].items():
								print(f'   {tag}: {value}')
						else:
							print('   No EXIF data found.')
			else:
				print("No files specified. In command-line mode, please provide file paths.")
				print("Usage: python scorpion.py [FILES...]")

if __name__ == "__main__":
	main()