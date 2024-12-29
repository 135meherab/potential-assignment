import os
import uuid
import zipfile
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, ImageOps, ImageSequence

from utils.helper import content_file_path


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CompressedImageFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        # Open image using PIL's open method (streaming)
        with Image.open(content) as image:
            # image = ImageOps.exif_transpose(image)
            img_io = BytesIO()

            try:
                # Check if the image is a GIF
                if image.format == "GIF":
                    self._process_gif(image, img_io)
                else:
                    self._process_image(image, img_io)

                # Use the file name generated by content_file_path function
                filename = self.field.get_content_file_path(self.instance, name)

                # Create a ContentFile from the BytesIO buffer
                image_content = ContentFile(img_io.getvalue())

                # Save the ContentFile
                super().save(filename, image_content, save)
            finally:
                img_io.close()

    def _process_gif(self, image, img_io):
        if getattr(image, "is_animated", False):
            frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
            if self.field.width and self.field.width < frames[0].width:
                frames = self._resize_frames(frames)
            frames[0].save(
                img_io,
                format="WEBP",
                save_all=True,
                append_images=frames[1:],
                duration=image.info.get("duration", 100),
                loop=image.info.get("loop", 0),
                quality=self.field.quality,
                method=6,
                lossless=False,
            )
        else:
            self._resize_and_save(image, img_io)

    def _process_image(self, image, img_io):
        if self.field.width and self.field.width < image.width:
            image = self._resize_image(image)
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            image.save(
                img_io,
                format="WEBP",
                optimize=True,
                quality=self.field.quality,
                lossless=False,
            )
        else:
            image.convert("RGB").save(
                img_io, format="WEBP", optimize=True, quality=self.field.quality
            )

    def _resize_frames(self, frames):
        aspect_ratio = frames[0].height / frames[0].width
        new_height = int(self.field.width * aspect_ratio)
        return [
            frame.resize((self.field.width, new_height), Image.Resampling.LANCZOS)
            for frame in frames
        ]

    def _resize_image(self, image):
        aspect_ratio = image.height / image.width
        new_height = int(self.field.width * aspect_ratio)
        return image.resize((self.field.width, new_height), Image.Resampling.LANCZOS)

    def _resize_and_save(self, image, img_io):
        if self.field.width and self.field.width < image.width:
            image = self._resize_image(image)
        image.save(img_io, format="WEBP", optimize=True, quality=self.field.quality)


class CompressedImageField(models.ImageField):
    attr_class = CompressedImageFieldFile

    def __init__(self, *args, quality=85, width=None, **kwargs):
        self.quality = quality
        self.width = width
        kwargs.setdefault("upload_to", self.get_content_file_path)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["quality"] = self.quality
        kwargs["width"] = self.width
        return name, path, args, kwargs

    @staticmethod
    def get_content_file_path(instance, filename):
        return content_file_path(instance, filename, file_extension="webp")