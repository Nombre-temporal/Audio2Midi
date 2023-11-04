# Import the necessary module
from setuptools import setup, find_packages

# Read the contents of the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Define package details
package_name = 'Audio2Midi'
package_version = '1.0'
package_description = 'Description of your package'

# Find all packages in the current directory
packages = find_packages()

# Set up the package
setup(
    name=package_name,
    version=package_version,
    description=package_description,
    packages=packages,
    install_requires=requirements,
)

# Inform the user about the setup process
print(f"Setting up the '{package_name}' package...")
print(f"Version: {package_version}")
print(f"Description: {package_description}")
print(f"Found packages: {', '.join(packages)}")
print("Installing required dependencies...")

# Installation is complete
print(f"The '{package_name}' package and its dependencies have been successfully installed.")
