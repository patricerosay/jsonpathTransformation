import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
    name="jsonpathTransformation",
    license='MIT',
    version="0.0.1",
    author="Bepeho",
    author_email="contact@bepeho.Com",
    description="A simple json to json transformation tool",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/patricerosay/jsonpathTransformation",
    packages=['jsonpathTransformation'],

    install_requires=[
          'jsonpath_ng','jsonpath_ng'
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "json",
    ),
    scripts=['bin/jpt','bin/jpe'],
    include_package_data=True,
    zip_safe=False
)