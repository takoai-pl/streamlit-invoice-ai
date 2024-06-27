from setuptools import setup, find_packages

setup(
    name='invoice_ai',
    version='0.1.1',
    url='https://github.com/takoai-pl/streamlit-invoice-ai.git',
    author='Maciej Tarasiuk',
    author_email='maciej.tarasiuk@takoai.pl, piotr.kazimierczak@takoai.pl',
    description='Invoice generator powered with the use of AI Agent made by TaKo AI.',
    packages=find_packages(),
    install_requires=[
        'streamlit==1.36.0',
        'sqlalchemy==2.0.31',
        'pydantic==1.10.13',
        'flask==3.0.1',
    ],
    extras_require={
        'dev': [
            'pytest==8.2.0',
            'pytest-asyncio==0.21.1',
            'mypy==1.4.1',
            'ruff==0.0.278',
            'black==23.7.0',
            'syrupy==4.0.2',
        ]
    },
)