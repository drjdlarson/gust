import setuptools


setuptools.setup(name='<NAME>',
                 version='0.0.0',
                 description='GUST plugin for <NAME>.',
                 long_description='',
                 url='',
                 author='<AUTHOR>',
                 author_email='',
                 license='GPL',
                 packages=setuptools.find_packages(),
                 install_requires=[
                                   # <REQUIREMENTS>
                                  ],
                 entry_points={"console_scripts": ["<NAME>=<NAME>.__main__:main"]},
                 include_package_data=True,
                 zip_safe=False)
