import logging
from whitenoise.storage import CompressedManifestStaticFilesStorage

logger = logging.getLogger("django")

class SafeCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except Exception as e:
            logger.warning(
                "Static post-processing: file '%s' referenced in '%s' not found. Falling back to original path.",
                name, filename
            )
            return name
