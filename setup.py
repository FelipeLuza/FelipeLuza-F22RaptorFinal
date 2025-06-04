# pip install cx_freeze
import cx_Freeze
executaveis = [
    cx_Freeze.Executable(script="main.py", icon="Recursos/icone.ico")
]

cx_Freeze.setup(
    name="Iron Man",
    version="1.0",
    description="Projeto final - Felipe Luza",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": ["Recursos"]
        }
    },
    executables=executaveis
)

# python setup.py build
# python setup.py bdist_msi
