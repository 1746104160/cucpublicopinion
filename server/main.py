'''
Descripttion: 业务管理系统
version: 1.0.0
Author: 邵佳泓
Date: 2022-07-08 01:17:46
LastEditors: 邵佳泓
LastEditTime: 2022-07-08 11:58:46
FilePath: /server/main.py
'''

from app import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
