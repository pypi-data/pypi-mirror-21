from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
  name = 'grattify',
  packages = ['grattify'],
  version = '0.2.9',
  description = 'Script to download music',
  author = 'Eric Taba',
  author_email = 'eptaba@gmail.com',
  url = 'https://github.com/etaba/grattify', # use the URL to the github repo
  download_url = 'https://github.com/etaba/grattify/tarball/0.1',
  keywords = ['music', 'spotify', 'pandora', 'download', 'song','youtube'], 
  classifiers = [],
  install_requires=[
        'bs4',
        'requests',
        'youtube_dl',
        'spotipy',
        'mutagen'
  ],
  scripts=['bin/grattify'],
  include_package_data=True
)

