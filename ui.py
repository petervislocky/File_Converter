from converters import ImageFile


def image_ui() -> None:
    path = input("Enter path of file to convert: ")
    ext = input("Enter the file format to convert to: ")
    print("Converting file...")
    converter = ImageFile(path)
    converter.convert(ext)
    print("Conversion complete!")
