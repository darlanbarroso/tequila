from roboflow import Roboflow
rf = Roboflow(api_key="vEk0o12j7gIkeAzeGObz")
project = rf.workspace("nuven").project("tequila")
version = project.version(3)
dataset = version.download("folder")

# MODIFICAR PRA UMA PASTA NO DRIVE (exemplo)