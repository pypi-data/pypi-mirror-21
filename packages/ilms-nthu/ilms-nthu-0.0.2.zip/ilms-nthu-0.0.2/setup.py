from distutils.core import setup

setup(
    name='ilms-nthu',
    packages=['ilms'],
    install_requires=[
        'requests'
    ],
    version='0.0.2',
    description='iLms-NTHU API. An iLMS client for stduents, assistants and developers.',
    author='leVirve',
    author_email='gae.m.project@gmail.com',
    url='https://github.com/leVirve/iLms-nthu-API',
    license='MIT',
    platforms='any',
    keywords=['iLms', 'NTHU', 'API'],
    classifiers=[],)
