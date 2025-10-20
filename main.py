from converters import ImageFile


def main():
    print(
        "File Converter\nStill in development, currently only supporting converting image files"
    )
    path = input("Enter path of file to convert: ")
    ext = input("Enter the file format to convert to: ")
    print("Converting file...")
    converter = ImageFile(path)
    converter.convert(ext)
    print("Conversion complete!")


if __name__ == "__main__":
    main()
