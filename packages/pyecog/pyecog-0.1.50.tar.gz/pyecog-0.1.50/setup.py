from distutils.core import setup
setup(
  name = 'pyecog',
  packages = ['pyecog', 'pyecog.ndf','pyecog.light_code', 'pyecog.visualisation'], # this must be the same as the name above
  version = '0.1.50',
  description = 'For classifying single channel ECoG recordings (iEEG)',
  author = 'Jonathan Cornford',
  author_email = 'jonathan.cornford@gmail.com',
  url = 'https://github.com/jcornford/pyecog', # use the URL to the github repo
  download_url = 'https://github.com/jcornford/pyecog/tarball/0.1.50',
  keywords = ['iEEG', 'ECoG'], # arbitrary keywords
  install_requires=['numpy','scipy','scikit-learn','jupyter' ,'pandas', 'matplotlib', 'seaborn','h5py','xlrd', 'bokeh', 'pyqtgraph', 'pomegranate'],
  entry_points={ 'gui_scripts': ['pyecog = pyecog.visualisation.pyecog_main_gui:main',] }
)
