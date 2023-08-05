from distutils.core import setup

setup(
    name='ssim',
    packages=['ssim'],
    package_dir={'ssim': 'ssim'},
    version='0.1.0',
    description='A parser for ssim',
    author='Rok Mihevc',
    author_email='rok.mihevc@gmail.com',
    url='https://github.com/rok/ssim',
    download_url='https://github.com/rok/ssim/archive/0.1.0.tar.gz',
    keywords=['parsing', 'ssim', 'data'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6'
    ]
)
