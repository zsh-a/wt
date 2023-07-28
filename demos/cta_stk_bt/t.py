from wtpy.monitor import WtBtSnooper
from wtpy import WtDtServo

def testBtSnooper():    

    dtServo = WtDtServo()
    dtServo.setBasefiles(folder="../../common")
    dtServo.setStorage(path='../storage')

    snooper = WtBtSnooper(dtServo)
    snooper.run_as_server(port=8081)

testBtSnooper()
