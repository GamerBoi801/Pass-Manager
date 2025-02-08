from setuptools import setup 

setup(
name="passm",
version="1.0",
py_modules=["main"],
install_requires=[
"typer[all]",
"bcrypt",
"pyfiglet",
"prettytable",],
entry_points={
"console_scripts": [
"password-manager=main:app",],
},
)
