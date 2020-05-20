import PyInstaller.__main__

package_name = "RoI V0.1"
data = "xml_spec.xsd:./"

PyInstaller.__main__.run([
    '--name=%s' % package_name,
    '--clean',
    '--windowed',
    '--onefile',
    '--add-data=%s' % data,
    'window_summary.py',
])
