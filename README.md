# dd列表提取器

for bilibili

生成列表可直接用于 [`DD监控室(DD_Monitor)`](https://github.com/zhimingshenjun/DD_Monitor)

# dd_extract.py（不登录版）

由于bilibili的限制，只能获取关注列表最近关注的250位和一开始关注的250位up主即**500位up主**中的vup

所以关注数少于500的b

站用户适用

## 使用方式

直接运行即可

```python
python3 dd_extract.py
```

然后跟着提示走，最后会输出你d的虚拟主播的名称和直播房间号

# dd_extract_with_login.py（扫码登录版）

关注数超过500的b

站用户只能登录后才能获取完整的关注列表

## 使用方式

直接运行即可

```python
python3 dd_extract_with_login.py
```

* 如果登录过，会自动读取存储在本地的cookie.txt文件，实现自动登录，**如果之后不再使用，请务必删除cookie.txt文件，防止信息泄露**

* 如果未曾登录，会弹出一个二维码，用手机bilibili扫描之后关闭窗口即可

等候一段时间之后自动登录成功并生成dd列表

# exe

相应名字的编译版

# 问题

如果出现问题，请提交issue

# 鸣谢

**thanks for https://github.com/zer0e/Bilibili-Api-Framework**