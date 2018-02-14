from setuptools import setup, find_packages

# Dynamically calculate the version based on django.VERSION.
version = __import__('mytils').get_version()

setup(
    name='django-mytils',
    version=version,
    description='Django small utils needed in every single project',
    author='Dmitry Akinin',
    author_email='d.akinin@gmail.com',
    url='https://github.com/applecat/django-mytils',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
)