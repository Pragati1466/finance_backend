import os
import magic
from typing import Tuple, Optional
from config.settings import settings
from config.logging import logger
from exceptions.exceptions import FileValidationError, InvalidFileTypeError, FileSizeExceededError


class FileValidator:
    # Comprehensive file validation for security and integrity
    
    # MIME type mappings for allowed file types
    MIME_TYPE_MAPPINGS = {
        'csv': ['text/csv', 'application/csv', 'text/plain'],
        'xlsx': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
        'xls': ['application/vnd.ms-excel', 'application/msexcel']
    }
    
    # Maximum file sizes in bytes
    MAX_FILE_SIZES = {
        'csv': 50 * 1024 * 1024,  # 50MB for CSV
        'xlsx': 100 * 1024 * 1024,  # 100MB for Excel
        'xls': 100 * 1024 * 1024   # 100MB for Excel
    }
    
    @classmethod
    def validate_file(cls, file_path: str, original_filename: str) -> Tuple[bool, Optional[str]]:
        # Validate file completely: size, type, content
        try:
            # Check file exists
            if not os.path.exists(file_path):
                return False, "File does not exist"
            
            # Check file size
            size_error = cls._validate_file_size(file_path, original_filename)
            if size_error:
                return False, size_error
            
            # Check file type
            type_error = cls._validate_file_type(file_path, original_filename)
            if type_error:
                return False, type_error
            
            # Check file content
            content_error = cls._validate_file_content(file_path)
            if content_error:
                return False, content_error
            
            logger.info(f"File validation passed: {original_filename}")
            return True, None
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return False, f"Validation error: {str(e)}"
    
    @classmethod
    def _validate_file_size(cls, file_path: str, filename: str) -> Optional[str]:
        # Validate file size against limits
        file_size = os.path.getsize(file_path)
        file_extension = cls._get_file_extension(filename)
        
        max_size = cls.MAX_FILE_SIZES.get(file_extension, settings.MAX_FILE_SIZE_MB * 1024 * 1024)
        
        if file_size > max_size:
            logger.warning(f"File size exceeded: {file_size} > {max_size}")
            return f"File size {file_size} bytes exceeds maximum allowed size {max_size} bytes"
        
        if file_size == 0:
            return "File is empty"
        
        return None
    
    @classmethod
    def _validate_file_type(cls, file_path: str, filename: str) -> Optional[str]:
        # Validate file type using MIME type detection
        file_extension = cls._get_file_extension(filename)
        
        if file_extension not in cls.MIME_TYPE_MAPPINGS:
            return f"File type '{file_extension}' is not supported"
        
        try:
            # Use python-magic for accurate MIME type detection
            mime = magic.Magic(mime=True)
            detected_mime = mime.from_file(file_path)
            
            allowed_mimes = cls.MIME_TYPE_MAPPINGS[file_extension]
            
            if detected_mime not in allowed_mimes:
                logger.warning(f"MIME type mismatch: {detected_mime} not in {allowed_mimes}")
                return f"File content type '{detected_mime}' does not match extension '{file_extension}'"
            
        except Exception as e:
            logger.warning(f"MIME type detection failed: {e}, falling back to extension validation")
            # Fallback to extension-only validation if magic fails
        
        return None
    
    @classmethod
    def _validate_file_content(cls, file_path: str) -> Optional[str]:
        # Validate file content for basic integrity
        try:
            # Check if file is readable
            with open(file_path, 'rb') as f:
                # Read first few bytes to check for corruption
                header = f.read(1024)
                if not header:
                    return "File appears to be corrupted or empty"
            
            return None
            
        except IOError as e:
            return f"File read error: {str(e)}"
    
    @classmethod
    def _get_file_extension(cls, filename: str) -> str:
        # Get file extension from filename
        return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        # Sanitize filename to prevent path traversal and other attacks
        # Remove path components
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        dangerous_chars = ['..', '/', '\\', '\0', '\n', '\r']
        for char in dangerous_chars:
            filename = filename.replace(char, '')
        
        # Limit filename length
        max_length = 255
        if len(filename) > max_length:
            filename = filename[:max_length]
        
        return filename
