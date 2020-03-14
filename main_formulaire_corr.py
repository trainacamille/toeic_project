import Application_vue
import sys


app = Application_vue.Application()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
