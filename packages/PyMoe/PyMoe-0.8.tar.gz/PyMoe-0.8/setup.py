from setuptools import setup

setup(
    name='PyMoe',
    version='0.8',
    packages=['Pymoe', 'Pymoe.Kitsu', 'Pymoe.VNDB', 'Pymoe.Mal', 'Pymoe.Bakatsuki'],
    url='https://github.com/ccubed/PyMoe',
    license='MIT',
    author='Cooper Click',
    author_email='ccubed.techno@gmail.com',
    description="PyMoe is the only lib you'll ever need if you need the animu or mangu on the Python Platform. It supports AniList, VNDB, Hummingbird and AniDB.",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    keywords="Anime Manga LN VN VNDB Anilist Kitsu AniDB MyAnimeList MAL Bakatsuki",
    install_requires=['requests', 'bs4', 'ujson']
)
