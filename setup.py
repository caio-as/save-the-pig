import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name="save the pig",
    options={'build_exe': {'packages':['pygame'],
                           'include_files': ['__pycache__', 'assets', 'public', 'sprites']}},
    executables = executables
)