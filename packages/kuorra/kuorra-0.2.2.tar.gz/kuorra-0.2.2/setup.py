from setuptools import setup, find_packages  # Always prefer setuptools over distutils

long_description = """
Create basic MVC skeleton using Web.py microframework and Heroku ready:
Functions:
    bootstrap - frontend framework
    jquery - js framework
    scheme.sql - MySQL demo database
    api - Restfull API
    ssl - HTTPS conection
    requirements.txt - Heroku requirements
    Procfile - Heroku config
"""

setup(
    name="kuorra",
    version="0.2.2",
    description="Create basic MVC skeleton using Web.py microframework",

    long_description=long_description,
    
    author="Salvador Hernandez Mendoza",
    
    author_email="salvadorhm@gmail.com",
    
    license="GPLv3",
    
    url="https://github.com/salvadorhm/kuorra",
    
    download_url="https://github.com/salvadorhm/kuorra",
    
    classifiers=['Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Topic :: Software Development',
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                'Programming Language :: Python :: 2.7'],
    keywords="mvc web.py mysql heroku bootstrap jquery ssl api restful",
    install_requires=["web.py==0.38", "MySQL-python==1.2.5", "pyOpenSSL==16.2.0"],
    zip_safe=False,

    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                    "tests", "*tests*"]),
    entry_points={'console_scripts': ['kuorra=kuorra.kuorra:main'],
                },
    package_data={"kuorra": [
            "__init__.py",
            "__main__.py",
            "kuorra.py",
            "model_generator.py",
            "api_generator.py",
            "plugin/model_master.py",
            "plugin/api_master.py",
            "mvc/__init__.py",
            "mvc/app.py",
            "mvc/Procfile",
            "mvc/requirements.txt",
            "mvc/Readme.md",
            "mvc/ssl",
            "mvc/ssl/server.crt",
            "mvc/ssl/server.csr",
            "mvc/ssl/server.key",
            "mvc/application/__init__.py",
            "mvc/application/controllers/__init__.py",
            "mvc/application/controllers/products/config.py",
            "mvc/application/controllers/products/delete.py",
            "mvc/application/controllers/products/edit.py",
            "mvc/application/controllers/products/index.py",
            "mvc/application/controllers/products/__init__.py",
            "mvc/application/controllers/products/insert.py",
            "mvc/application/controllers/products/view.py",
            "mvc/application/models/config.py",
            "mvc/application/models/__init__.py",
            "mvc/application/models/model_products.py",
            "mvc/application/views/__init__.py",
            "mvc/application/views/products/delete.html",
            "mvc/application/views/products/edit.html",
            "mvc/application/views/products/index.html",
            "mvc/application/views/products/__init__.py",
            "mvc/application/views/products/insert.html",
            "mvc/application/views/products/master.html",
            "mvc/application/views/products/view.html",
            "mvc/application/api/__init__.py",
            "mvc/application/api/products/__init__.py",
            "mvc/application/api/products/api_products.py",
            "mvc/application/api/products/config.py",
            "mvc/data/schema.sql",
            "mvc/static/css/bootstrap.css",
            "mvc/static/css/index.html",
            "mvc/static/files/default.jpg",
            "mvc/static/fonts/glyphicons-halflings-regular.eot",
            "mvc/static/fonts/glyphicons-halflings-regular.svg",
            "mvc/static/fonts/glyphicons-halflings-regular.ttf",
            "mvc/static/fonts/glyphicons-halflings-regular.woff",
            "mvc/static/fonts/glyphicons-halflings-regular.woff2",
            "mvc/static/fonts/index.html",
            "mvc/static/js/bootstrap.js",
            "mvc/static/js/index.html",
            "mvc/static/js/jquery.js"]}
)