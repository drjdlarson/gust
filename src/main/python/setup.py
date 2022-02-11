import setuptools


setuptools.setup(name='gust',
                 version='0.0.0',
                 description='GCS for UAS Swarming and Teaming (GUST).',
                 long_description='',
                 url='https://github.com/drjdlarson/gust/',
                 author='Laboratory for Autonomy GNC and Estimation Research (LAGER)',
                 author_email='',
                 license='GPL',
                 packages=setuptools.find_packages(),
                 install_requires=['flask', 'flask-restx', 'requires', 'pyqt5'],
                 include_package_data=True,
                 zip_safe=False)
