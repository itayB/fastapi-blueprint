import uvicorn

from app.settings import Settings


def main() -> None:
    settings = Settings()
    uvicorn.run("app.main:app", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
