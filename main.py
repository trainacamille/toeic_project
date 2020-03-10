import application
import application_aide
import sys


app = application.Application()
app2 = application_aide.Application("qccm.png",198)
app3 = application_aide.Application("qccm.png",199)
exit_status = app2.run(sys.argv)
exit_status2 = app3.run(sys.argv)
sys.exit(exit_status)
sys.exit(exit_status2)
