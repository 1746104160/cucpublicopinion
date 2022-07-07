<!--
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:49
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:55:57
 * @FilePath: /server/home/sjh/software/readme.md
-->
# 业务管理系统

## 前端
```bash
# 切换到前端项目路径
cd app

# 安装命令，推荐yarn
npm install  / yarn

# 开发环境会在本地启动一个服务器，地址是http://localhost:8080/
npm run dev / yarn dev

# 打包
npm run build / yarn build
```

## 后端

```bash
# 切换到后端端项目路径
cd server

# 安装命令
conda env create -f env.yml
sudo apt install -y uwsgi uwsgi-plugin-python3
# 启动后端服务器，地址是http://127.0.0.1:5000/
uwsgi -i uwsgi.ini
```
