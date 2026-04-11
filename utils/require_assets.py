from pathlib import Path


def require_assets_structure() -> None:
    '''
    Create required assets directories.
    '''

    required_directories = {
        Path("assets"),
        Path("assets/json"),
        Path("assets/images"),

        Path("assets/images/converted"),
        Path("assets/images/converted/dashboard"),
        Path("assets/images/converted/default"),
        Path("assets/images/converted/nasa"),

        Path("assets/images/temp"),
    }

    for directory in required_directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    require_assets_structure()
    print("Assets structure is ready.")