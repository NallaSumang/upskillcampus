"""
Custom exception classes and FastAPI exception handlers.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AssetNotFoundError(Exception):
    """Raised when an asset with the given ID does not exist."""

    def __init__(self, asset_id: int):
        self.asset_id = asset_id
        self.message = f"Asset with id {asset_id} not found"
        super().__init__(self.message)


class DuplicateAssetError(Exception):
    """Raised when attempting to create a duplicate asset."""

    def __init__(self, machine_name: str):
        self.machine_name = machine_name
        self.message = f"Asset '{machine_name}' already exists"
        super().__init__(self.message)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach custom exception handlers to the FastAPI application."""

    @app.exception_handler(AssetNotFoundError)
    async def asset_not_found_handler(
        request: Request, exc: AssetNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": "not_found",
                "message": exc.message,
                "asset_id": exc.asset_id,
            },
        )

    @app.exception_handler(DuplicateAssetError)
    async def duplicate_asset_handler(
        request: Request, exc: DuplicateAssetError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "error": "conflict",
                "message": exc.message,
            },
        )
