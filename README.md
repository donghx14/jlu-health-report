# jlu-health-report



吉林大学研究生自动健康打卡

- **自动获取并填入个人信息**
- 使用request直接发起请求
- 定时自动打卡
- 支持多用户

# 使用方法

**若打卡系统页面更新，只需手动在打卡页面填入并提交一次，之后即可重新运行打卡程序，无需对程序进行修改**

- **单用户脚本模式**

```
python main.py --user [YourUsername] --pwd [YourPassword]
```

- **手动模式**

1. 填写`users.py`中一个或多个用户的用户名与密码
2. 运行`main.py`


- **定时自动模式**

1. 填写`users.py`中一个或多个用户的用户名与密码 
2. 运行`auto.py`，需要常驻后台

# 参考

[https://github.com/Venquieu/DBM](https://github.com/Venquieu/DBM)

https://github.com/HORIZONNN/jlu_check



