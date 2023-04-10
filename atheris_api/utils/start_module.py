# Python imports
import keyword
import os
import re
import sys


class StartModule:
    def __init__(self, module_name: str) -> None:
        self.__module_name: str = module_name
        self.__pattern: str = r"^[a-zA-Z_][a-zA-Z0-9_]*$"

    def get_module_path(self) -> str:
        if bool(re.match(self.__pattern, self.__module_name)) and not keyword.iskeyword(
            self.__module_name
        ):
            module_path = os.path.join(
                os.getcwd(), "atheris_api", "modules", self.__module_name
            )
            if not os.path.exists(module_path):
                return module_path
            else:
                raise ValueError(
                    f"""
The module name is invalid
    ■ A module with the name {self.__module_name} already exists.
"""
                )
        else:
            raise ValueError(
                """
The module name is invalid:
    ■ The module name must begin with a letter or an underscore.
    ■ Allowed characters in the rest of the name are letters, digits and underscores.
    ■ The name cannot be a Python keyword (e.g., if, else, for, etc.).
"""
            )

    def create_module(self) -> None:
        module_path: str = self.get_module_path()
        os.makedirs(module_path)
        open(os.path.join(module_path, "__init__.py"), "a").close()
        subdirectories = ["services", "models", "schemas", "routes"]
        for subdir in subdirectories:
            subdir_path = os.path.join(module_path, subdir)
            os.makedirs(subdir_path, exist_ok=True)
            open(os.path.join(subdir_path, "__init__.py"), "a").close()


def start():
    if len(sys.argv) == 2 and sys.argv[0] == "startmodule":
        module = StartModule(sys.argv[1])
        try:
            module.create_module()
        except Exception as e:
            print(e)
