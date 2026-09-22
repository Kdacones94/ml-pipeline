class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass

class SchemaValidationError(PipelineError):
    """Raised when incoming data violates target schema expectations."""
    pass

class MatrixShapeError(PipelineError):
    """Raised when feature matrix dimension is not 3x3."""
    pass
