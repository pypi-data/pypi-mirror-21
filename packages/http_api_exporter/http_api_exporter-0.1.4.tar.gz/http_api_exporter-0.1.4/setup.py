from distutils.core import setup

setup(
  name = 'http_api_exporter',
  packages = ['http_api_exporter'],
  version = '0.1.4',
  description = 'A simple api exporter for py',
  author = 'Sraw',
  author_email = 'lzyl888@gmail.com',
  url = 'https://github.com/Sraw/http_api_exporter', 
  download_url = 'https://github.com/Sraw/http_api_exporter/tarball/0.1.4', 
  keywords = ['http', 'web', 'api', 'export'], # arbitrary keywords
  classifiers = [
      'Programming Language :: Python :: 3'
    ],
  install_requires=[
          'tornado',
      ],
)
