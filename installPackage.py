import pip

# Checking PIP
print(pip.__version__)
print(pip.__dict__)

# Define the package name you want to install
package_name = "matplotlib"

# Run the pip command to install the package
#subprocess.call([bpy.app.binary_path_python, '-m', 'pip', 'install', package_name])
pip.main(['install', package_name, '--user'])