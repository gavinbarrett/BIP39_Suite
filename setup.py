import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
	name="bip-tools", 
	version="1.0.4", 
	description="Manage BIP32 based HD wallets.",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/gavinbrrtt/biptools",
	author="Gavin Barrett",
	author_email="gavinbrrtt@gmail.com",
	license="GPLv3",
	classifiers=[
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.8",
	],
	install_requires=["base58"],
	include_package_data=True,
	packages=["biptools"],
)
