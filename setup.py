from setuptools import setup, find_packages

def get_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name='data_interaction_client',
    version='1.0.0',
    description='Клиент взаимодействия с источниками данных Python пакет, который предоставляет коннекторам клиент для взаимодействия с платформой.',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='Быков Дмитрий',
    author_email='termityabk@bk.ru',
    url='https://github.com/termityabk/DataInteractionClient',
    packages=find_packages(),
    install_requires=[
        'httpx==0.27.0',
        'pydantic==1.8.2',
        'asyncio==3.4.3',
    ],
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10.14',
    ],
    python_requires=">=3.10",
)
