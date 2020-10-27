
import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute(''' drop table blog_Recommend ''')
# c.execute(''' insert into  polls_question (id, question_text, pub_date) values (6, 'test' ,'19000101')''')
# c.execute("commit")
# conn.close()

##--------------------------------------------------------------------------------------------
## 데이터프레임을 DB에 저장.

import pandas as pd
df = pd.read_csv("C:/Django/pjt/Rec/Recommend.csv")
print( df )
#
df.to_sql('blog_Recommend', conn ,if_exists='append' , index=True )
# df.to_sql('test', conn ,if_exists='fail' )
# help(pd.DataFrame.to_sql)

#DataFrame.to_sql(name, con, flavor='sqlite', schema=None, \ if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)


###--------------------------------------------
#관리자 권한 실행
# import sys
# import os
# import win32com.shell.shell as shell
#
# if sys.argv[-1] != 'asadmin':
#     script = os.path.abspath(sys.argv[0])
#     params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
#     shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
#
#
#     import ctypes
#     if ctypes.windll.shell32.IsUserAnAdmin():
#         print('관리자권한으로 실행된 프로세스입니다.')
#     else:
#         print('일반권한으로 실행된 프로세스입니다.')
#     #sys.exit(0)
#
#
# ###--------------------------------------------
# #관리자 권한 실행 여부 알아내기
# import ctypes
#
# if ctypes.windll.shell32.IsUserAnAdmin():
#     print('관리자권한으로 실행된 프로세스입니다.')
# else:
#     print('일반권한으로 실행된 프로세스입니다.')