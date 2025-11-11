from abc import ABC, abstractmethod
from pathlib import Path

import magic
import pypandoc
from PIL import Image


class BaseFileConverter(ABC):
    """Base class for all other converter classes to inherit from

    MIME_TYPE is the allowed input file formats
    SUPPORTED_FORMATS is the allowed output file formats
    """

    MIME_TYPE: tuple
    SUPPORTED_FORMATS: dict[str, str]

    def __init__(self, file: Path) -> None:
        self.mime = magic.Magic(mime=True)
        self._validate_file_type(file)
        self.file = file

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        required_attrs = ["MIME_TYPE", "SUPPORTED_FORMATS"]
        missing_attrs = [attr for attr in required_attrs if attr not in cls.__dict__]
        if missing_attrs:
            missing = ", ".join(missing_attrs)
            raise TypeError(f"{cls.__name__} must define {missing}")

    @abstractmethod
    def convert(self, extension: str) -> Path:
        """Override and use to convert file to given extension"""
        pass

    def _validate_file_type(self, file: Path) -> None:
        """Validates that the mime format of the given file is allowed for the
        converter class it is being passed to
        """
        file_type = self.mime.from_file(file)

        for allowed in self.MIME_TYPE:
            if file_type.startswith(allowed):
                return

        raise ValueError(
            f"Only {', '.join(self.MIME_TYPE)} file types can be passed to this object"
        )

    def _validate_extension(self, extension: str) -> str:
        """Formats the extension given for internal class use"""
        ext = extension.lower().lstrip(".")
        supported = ",".join(self.SUPPORTED_FORMATS.keys())
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {extension}\nSupported formats: {supported}"
            )
        return self.SUPPORTED_FORMATS[ext]


class ImageFile(BaseFileConverter):
    """One file is meant to be given to an instance of this class, and then
    operations can be repeatedly executed on the same base file.

    To do operations on a new file, make a new instance.
    """

    MIME_TYPE = ("image/",)
    SUPPORTED_FORMATS = {
        "jpeg": ".jpg",
        "jpg": ".jpg",
        "png": ".png",
        "webp": ".webp",
        "bmp": ".bmp",
        "gif": ".gif",
        "pdf": ".pdf",
    }

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


class DocConverter(BaseFileConverter):
    """For converter document file formats to other document file formats"""

    def __init__(self, file: Path) -> None:
        super().__init__(file)
        try:
            import pypandoc

            self.pypandoc = pypandoc
            self.HAS_PYPANDOC = True
        except ImportError:
            self.pypandoc = None
            self.HAS_PYPANDOC = False
            print("Pandoc and pypandoc must be installed to convert document formats")
            print("Install Pandoc with your package manager or from the Pandoc website")
            print("Install pypandoc with `pip install pypandoc`")

    MIME_TYPE = (
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plainapplication/rtf",
        "text/csv",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.oasis.opendocument.spreadsheet",
        "application/vnd.oasis.opendocument.presentation",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    SUPPORTED_FORMATS = {
        ".docx": "docx",
        ".doc": "doc",
        ".pdf": "pdf",
        ".txt": "txt",
        ".md": "md",
        ".csv": "csv",
    }

    def convert(self, extension: str):
        """Converts file to `extension` format

        Args:
            extension: the type of file to convert to, supports `.ext` or `ext`
        """
        if not self.HAS_PYPANDOC:
            raise RuntimeError("pypandoc not available, cannot convert document")

        return pypandoc.convert_file(
            self.file, extension, outputfile=f"output.{extension}"
        )
