from setuptools import setup
import platform, warnings

#Pypy dependency support
python_implementation = platform.python_implementation()

#install_requires = ['sqlalchemy', 'pymysql', 'psycopg2',]
install_requires = ['sqlalchemy',]
if python_implementation == "PyPy":
    #install_requires = ['sqlalchemy', 'pymysql', 'psycopg2cffi',]
    install_requires = ['sqlalchemy',] 
elif python_implementation != "CPython":
    warnings.warn("We don't know how to deal with the {} runtime. Treating it like CPython".format(python_implementation), RuntimeWarning)

setup(name='sqlcurses',
        version='0.1.5',
        description='console based database editor',
        url='http://github.com/laijsonk/sqlcurses',
        author='Jason K Lai',
        author_email='laijasonk@gmail.com',
        license='GNU',
        scripts=['bin/sqlcurses',],
        packages=['sqlcurses',],
        install_requires=install_requires,
        include_package_data=True
)
