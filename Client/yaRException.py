from enum import Enum, auto

class yaRErrorCodes(Enum):
    AUDIO_RECORDING_FAILED = auto()
    VIDEO_UPLOAD_URL_NOT_FOUND = auto()
    VIDEO_UPLOAD_TOKEN_NOT_FOUND = auto()
    VIDEO_FILE_NOT_FOUND_WHILE_UPLOAD = auto()
    AUDIO_FILE_NOT_FOUND_WHILE_UPLOAD = auto()
    VIDEO_PROCESSING_FAILED = auto()


class yaRErrorCodesMapping:
    """
    Mappings of error codes to error messages.
    """
    error_codes = {
        yaRErrorCodes.AUDIO_RECORDING_FAILED: "Audio recording failed.",
        yaRErrorCodes.VIDEO_UPLOAD_URL_NOT_FOUND: "API URL not found in environment variables.",
        yaRErrorCodes.VIDEO_UPLOAD_TOKEN_NOT_FOUND: "API token not found in environment variables.",
        yaRErrorCodes.VIDEO_FILE_NOT_FOUND_WHILE_UPLOAD: "The video file does not exist.",
        yaRErrorCodes.AUDIO_FILE_NOT_FOUND_WHILE_UPLOAD: "The audio file does not exist.",
        yaRErrorCodes.VIDEO_PROCESSING_FAILED: "Video processing failed."
    }


class yaRException(Exception):
    """
    A custom exception class for handling application-specific errors. This class can be used for raising exceptions for scenarios that are specific to yaR's functionality. 

    """

    def __init__(self, error_type):
        self.error_type = error_type
        self.message = yaRErrorCodesMapping.error_codes[error_type]
        super().__init__(self.message)

    def __str__(self):
        return self.message