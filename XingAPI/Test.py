from ctypes import *
import os

from XingAPI.Xing_LogIn import XSession

#xaCommonDll = windll.LoadLibrary(os.path.abspath("XA_Common.dll"))
#xaSessionDll = windll.LoadLibrary(os.path.abspath("XA_Session.dll"))
#xaDataSetDll = windll.LoadLibrary(os.path.abspath("XA_DataSet.dll"))

xsession = XSession.get_instance()
xsession.api_login()
xsession.account_info()



