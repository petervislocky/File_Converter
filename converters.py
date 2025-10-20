import magic
from PIL import Image
from pathlib import Path


class ImageFile:
    """One file is meant to be given to an instance of this class, and then
    operations can be repeatedly executed on the same base file.

    To do operations on a new file, make a new instance.
    """

    SUPPORTED_FORMATS = {
        "jpeg": ".jpg",
        "jpg": ".jpg",
        "png": ".png",
        "webp": ".webp",
        "bmp": ".bmp",
        "gif": ".gif",
        "pdf": ".pdf",
    }

    def __init__(self, file: str) -> None:
        self.mime = magic.Magic(mime=True)
        self._validate_file_type(file)
        self.file = file

    def convert(self, extension: str) -> Path:
        """Converts image file to given extension.

        Args:
            extension: File extension name to convert to.
        """
        img = Image.open(self.file)
        dot_ext = self._validate_extension(extension)

        if dot_ext == ".jpg":
            img = self._convert_to_rgb(img)

        input_path = Path(self.file)
        output_path = input_path.with_suffix(dot_ext)
        img.save(output_path, extension.upper())

        return output_path

    def _convert_to_rgb(self, img: Image.Image) -> Image.Image:
        """Internal method to convert from transparency supporting color formats
        to standard RGB
        """
        if img.mode in ("RGBA", "LA", "P"):
            return img.convert("RGB")
        else:
            return img

    def _validate_file_type(self, file: str) -> None:
        """Validates that file is an image file, raises ValueError if not"""
        file_type = self.mime.from_file(file)
        if not file_type.startswith("image/"):
            raise ValueError("Only image files can be passed to this object")

    def _validate_extension(self, extension: str) -> str:
        """Formats the extension given for internal class use"""
        ext = extension.lower().lstrip(".")
        supported = ",".join(self.SUPPORTED_FORMATS.keys())
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {extension}\nSupported formats: {supported}"
            )
        return self.SUPPORTED_FORMATS[ext]


if __name__ == "__main__":
    png_file = r"/home/recluse/Downloads/feather.png"
    converter = ImageFile(png_file)
    converter.convert("pdf")
