activate_this = 'C:/python/flaskbase/Scripts/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import site
import sys

# Remember original sys.path.
prev_sys_path = list(sys.path)
# Add site-packages directory.
site.addsitedir('C:/python/flaskbase/Lib/site-packages')
# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
        sys.path[:0] = new_sys_path
sys.path.insert(0, 'C:/CODE/PYTHON/WebDeom_Flask')

from manage import app

application = app
