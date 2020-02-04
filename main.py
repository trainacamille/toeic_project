import application
import sys


app = application.Application()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
