"""Common data models."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """Kubernetes-style metadata."""

    name: str = Field(..., description="Resource name (unique identifier)")
    labels: Dict[str, str] = Field(default_factory=dict, description="Resource labels")
    annotations: Dict[str, str] = Field(default_factory=dict, description="Resource annotations")
    creationTimestamp: Optional[datetime] = Field(None, description="Creation timestamp")
    deletionTimestamp: Optional[datetime] = Field(None, description="Deletion timestamp")
    version: Optional[int] = Field(None, description="Resource version")


class ListResult(BaseModel):
    """Generic list result."""

    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    total: int = Field(..., description="Total number of items")
    items: List[Any] = Field(default_factory=list, description="List of items")
    first: bool = Field(..., description="Is first page")
    last: bool = Field(..., description="Is last page")
    hasNext: bool = Field(..., description="Has next page")
    hasPrevious: bool = Field(..., description="Has previous page")
    totalPages: int = Field(..., description="Total number of pages")


class ErrorResponse(BaseModel):
    """Error response from API."""

    status: int = Field(..., description="HTTP status code")
    type: str = Field(..., description="Error type")
    title: str = Field(..., description="Error title")
    detail: Optional[str] = Field(None, description="Error detail")
    instance: Optional[str] = Field(None, description="Error instance")
    timestamp: Optional[datetime] = Field(None, description="Error timestamp")


class ToolResult(BaseModel):
    """Result from MCP tool execution."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Result message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")

    @classmethod
    def success_result(cls, message: str, data: Optional[Dict[str, Any]] = None) -> "ToolResult":
        """Create a success result."""
        return cls(success=True, message=message, data=data)

    @classmethod
    def error_result(cls, message: str, data: Optional[Dict[str, Any]] = None) -> "ToolResult":
        """Create an error result."""
        return cls(success=False, message=message, data=data)
