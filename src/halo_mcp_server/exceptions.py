"""Halo MCP 服务器自定义异常"""


class HaloMCPError(Exception):
    """Halo MCP 服务器基础异常"""

    def __init__(self, message: str, details: dict = None):
        """
        初始化异常。

        参数:
            message: 错误信息
            details: 额外的错误细节
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(HaloMCPError):
    """认证失败"""

    pass


class AuthorizationError(HaloMCPError):
    """授权/权限拒绝"""

    pass


class ResourceNotFoundError(HaloMCPError):
    """资源未找到"""

    def __init__(self, resource_type: str, name: str):
        """
        初始化资源未找到异常。

        参数:
            resource_type: 资源类型
            name: 资源名称
        """
        super().__init__(f"未找到资源 {resource_type} '{name}'")
        self.resource_type = resource_type
        self.name = name


class ValidationError(HaloMCPError):
    """数据校验错误"""

    pass


class NetworkError(HaloMCPError):
    """网络/HTTP 错误"""

    def __init__(self, message: str, status_code: int = None, details: dict = None):
        """
        初始化网络错误。

        参数:
            message: 错误信息
            status_code: HTTP 状态码
            details: 额外错误细节
        """
        super().__init__(message, details)
        self.status_code = status_code


class ConfigurationError(HaloMCPError):
    """配置错误"""

    pass


class OperationError(HaloMCPError):
    """操作失败"""

    pass
