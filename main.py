from pathlib import Path

from converters import ImageFile


def main():
    # Testing UI only
    print("File Converter")
    print("Still in development, current UI is for testing purposes only")

    entered_path = input("Enter path of file to convert: ")
    path = Path(entered_path).expanduser()
    ext = input("Enter the file format to convert to: ")
    print("Converting file...")
    converter = ImageFile(path)
    converter.convert(ext)
    print("Conversion complete!")


if __name__ == "__main__":
    main()
