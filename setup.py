import os
from distutils.core import setup

# to recusively include all files under app templates and static
app_data_dir = ['SpearmintServer/app/templates', 'SpearmintServer/app/static']
app_data_files = []
for l in app_data_dir:
    for r, d, files in os.walk(l):
        len_prefix = len('SpearmintServer/app/') # to remove the prefix from path
        app_data_files += [os.path.join(r[len_prefix:], f) for f in files]

setup(name='SpearmintServer',
      description='Spearmint Django application',
      version='0.9.3',
      author='J. Lee',
      author_email='jinho89@gmail.com',
      #package_dir={'': 'SpearmintServer'},
      packages=['SpearmintServer',
                'SpearmintServer.app',
                'SpearmintServer.app.templatetags',
                'SpearmintServer.api',
               ],
      package_data={'SpearmintServer.app': app_data_files},
      install_requires=['Django==1.6.0',
                        'South==0.8.4',
                        'MySQL-Python==1.2.5',
                        'python-dateutil>=1.5',
                        'django-oauth-toolkit==0.9.0',
                        'django-cors-headers==1.1.0',
                       ],
     )
