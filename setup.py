from setuptools import setup, find_packages

# setup(
#     name="tuiqiao",
#     version="0.3.0",
#     author="Daolin Han",
#     author_email="2862308357@qq.com",
#     description=("a spelling correction tool for Chinese"),
#     license="MIT Licence",
#     url="https://github.com/HDL951236874/tuiqiao",
#     package_dir={'tuiqiao':'tuiqiao'},
#     packages=['tuiqiao', 'tuiqiao.utils', 'tuiqiao.data'],
#     package_data={'jieba':['*.*','finalseg/*','analyse/*','posseg/*']
#     include_package_data=True,
#     paltforms="any"
# )
setup(
    name = "tuiqiao",
    version = "0.6.0",
    author = "Daolin Han",
    author_email = "2862308357@qq.com",
    description=("a spelling correction tool for Chinese"),
    license = "MIT Licence",
    url="https://github.com/HDL951236874/tuiqiao",

    package_dir={'tuiqiao':'tuiqiao'},
    packages=['tuiqiao','tuiqiao.utils','tuiqiao.data'],
    package_data={'tuiqiao':['*.*','data/*','utils/*']},
    # include_package_data = True,
    # paltforms = "any"
)
