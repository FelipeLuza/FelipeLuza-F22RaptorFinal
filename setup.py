from cx_Freeze import setup, Executable

build_options = {
    "packages": ["pygame", "pyttsx3", "speech_recognition", "pyaudio"],
    "include_files": [("Recursos", "Recursos")]  
}

executables = [
    Executable(
        script="main.py",  
        base=None
    )
]

setup(
    name="F-22 Raptor: Zona de Combate",
    version="1.0",
    description="Projeto final - Felipe Luza",
    options={"build_exe": build_options},
    executables=executables
)
