"# LanguageExtract" 

# 当前脚本执行流程简介：
# 1.开发人员运行脚本 python python/LanguageExtract.py 指定的res文件夹路径(例如：D:\project\workspace\tvtWorkSpace\NVMS2.1.x\NVMS_3.0.1\f-tvt-base\src\main\res)
# 2.通过脚本方式，自动提取指定Module中的res下的value-zh-rCN下的strings.xml文件的所有值，输出到一个res/tempFile/jt.txt文件中，Terminal等待用户确认
# 3.开发人员将res/tempFile/jt.txt的内容丢到网页翻译，简体->繁体
# 4.开发人员将翻译后的结果，复制回res/tempFile/ft.txt文件中
# 5.开发人员在Terminal中输入yes，确定已将翻译后的内容复制到ft.txt中
# 6.脚本自动根据res/tempFile/ft.txt的内容，创建values-zh-rTW和values-zh-rHK文件夹，并创建文件夹下的strings.xml文件
# 7.脚本根据res/tempFile/ft.txt的内容，自动在strings.xml创建string标签对，生成繁体语种标签
