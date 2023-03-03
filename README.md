# XMind2TestCasePro
<img src="https://user-images.githubusercontent.com/77818535/222654148-4959af6b-cb31-48f0-af4b-fed92a016087.png" width="50%">

## 1. 区别
[xmind2testcase](https://github.com/zhuifengshen/xmind2testcase/tree/master/xmind2testcase)与[xmind2testcasepro](https://github.com/goehls/xmind2testcasepro)的区别：

- 支持新版本的xmind文件的解析，同时支持旧版本的xmind文件的解析
- 用例的展示更加丰富，更加精细。
   - 在保持testcase title的前提下，将非testcase节点的部分提取为Category
   - 不同节点的title链接的展示优化
- 测试模板支持一个测试步骤包含多个预期结果。


## 2. 测试用例模板

### 2.1 用例模板
[新的用例模板](docs/new/)
[[公众号：波小艺] 测试用例 模版.xmind](docs%2Fnew%2F%5B%E5%85%AC%E4%BC%97%E5%8F%B7%EF%BC%9A%E6%B3%A2%E5%B0%8F%E8%89%BA%5D%20%E6%B5%8B%E8%AF%95%E7%94%A8%E4%BE%8B%20%E6%A8%A1%E7%89%88.xmind)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/2519304/1677761843585-c6d86a15-53f6-4686-ad7f-02b18da22619.png#averageHue=%23fdfcfc&clientId=uc02f5cde-05a5-4&from=paste&height=942&id=uf561cec7&name=image.png)<br />标签（label）：**测试用例**、**执行步骤、预期结果**、**前置条件**、**优先级**标签（如：P1）<br />标记（marker）：优先级标记，label优先级更高<br />备注：summary。测试用例节点才会被解析。


### 2.2 模板解析规则

- 中心主题默认为产品名称
- 中心主题的第一层会被识别为`testsuite`
- 包含`测试用例`标签的节点的会识别为`testcase`
- `testsuite`- `testcase`之间的节点title被识别为用例的分类（Category）
- `testcase`的子主题包含`前置条件`标签的为`PreConditions`、包含`执行步骤`标签的为`teststep`
- `teststep`的子主题包含`预期结果`标签的为`ExpectResults`，一个执行步骤可以包含多个预期结果。
- `testcase`的优先级可用marker进行标记。也可以通过label进行标记（如P0，priority 1），label的优先级更高
- `testcase`的执行类型通过label定义：`手动`、`自动`。默认为`手动`。
- `testcase`的摘要summary通过`testcase`节点的备注记录
- `testcase`节点包含`ignore`标签时，会被打上一个`ignore`的标记
- 自由主题不会被解析

## 3. 模板解析结果
`xmind2testcasepro`解析并渲染到前端的结果如下：

![image.png](https://cdn.nlark.com/yuque/0/2023/png/2519304/1677759304021-a8de7581-10e8-4b3f-83d2-671a72594da4.png)

- Suite表示模块名称。
- Category表示**模块节点**到**测试用例节点**中间包含的这些节点的集合。
- Title表示测试用例名称。
- PreConditions表示前置条件，可以包含多个。
- Attributes包含用例的优先级priority，测试用例节点的备注summary。
- Steps表示执行步骤以及预期结果，一个执行步骤可对应多个预期结果。
- 对于无效的用例，忽略的用例，用户可以选择是否将其展示出来。

## 4. 使用示例
### 4.1 安装方式
```
pip3 install xmind2testcasepro
```


### 4.2 版本升级
```
pip3 install -U xmind2testcasepro
```

### 4.3 命令行
```
Usage:
 xmind2testcasepro [path_to_xmind_file] [-csv] [-xml] [-json]

Example:
 xmind2testcasepro /path/to/testcase.xmind        => output testcase.csv、testcase.xml、testcase.json
 xmind2testcasepro /path/to/testcase.xmind -csv   => output testcase.csv
 xmind2testcasepro /path/to/testcase.xmind -xml   => output testcase.xml
 xmind2testcasepro /path/to/testcase.xmind -json  => output testcase.json
```

### 4.4 Web页面
```
Usage:
 xmind2testcasepro [webtool] [port_num]

Example:
 xmind2testcasepro webtool        => launch the web testcase convertion tool locally -> 127.0.0.1:5001
 xmind2testcasepro webtool 8000   => launch the web testcase convertion tool locally -> 127.0.0.1:8000
```

### 4.5 API调用
[view samples.py](samples.py)


## 5. 其他功能
* XMind用例文件转为JSON数据（与原有工具保持一致）
  * (1)转为TestCase JSON数据
  * (2)转为TestSuite JSON数据
  * (3)XMind文件转换为JSON数据
  


## 6. 使用示例
1、Web工具示例
![webtool](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/webtool.png)
2、转换后用例预览
![testcase_preview](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/xmind_to_testcase_preview.png)
3、TestLink导入结果示例
![testlink](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/testlink.png)
4、禅道（ZenTao）导入结果示例
![zentao](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/zentao_import_result.png)



## 7. 自动化发布：一键打 Tag 并上传至 PYPI 

每次在 __ about __.py 更新版本号后，运行以下命令，实现自动化更新打包上传至 [PYPI](https://pypi.org/) ，同时根据其版本号自动打 Tag 并推送到仓库：

```
python3 setup.py pypi
```

![upload_pypi](https://raw.githubusercontent.com/zhuifengshen/xmind2testcase/master/webtool/static/guide/pypi_upload.png)


## 8. CHANGELOG

```
v1.0.0
1、XMind用例模板定义和解析；
2、XMind用例转换为TestLink用例文件；

v1.1.0
1、XMind用例文件转换为禅道用例文件；
2、添加一键上传PYPI功能；

v1.2.0
1、添加Web工具进行用例转换；
2、添加用户使用指南；

v1.3.0
1、XMind中支持标识测试用例执行结果；
2、TestCase、TestSuite中添加用例执行结果统计数据；
3、完善用户使用指南；

v1.5.0
1、支持通过标签设置用例类型（自动 or 手动）；
2、支持导出文件中文显示；
3、增加命令运行指引；
4、修复服务器远程部署无法访问问题；
5、取消测试用例关键字默认设置；

v2.0.0
1、支持xmind新版本文件的解析
2、针对新版本的xmind文件的用例格式优化
3、支持一个测试步骤包含多个预期结果的解析
```

## 9. 额外信息
### XMind2TestCase工具的背景 （[背景来源](https://github.com/zhuifengshen/xmind2testcase)）

软件测试过程中，最重要、最核心就是测试用例的设计，也是测试童鞋、测试团队日常投入最多时间的工作内容之一。

然而，传统的测试用例设计过程有很多痛点：
- 1、使用Excel表格进行测试用例设计，虽然成本低，但版本管理麻烦，维护更新耗时，用例评审繁琐，过程报表统计难...
- 2、使用TestLink、TestCenter、Redmine等传统测试管理工具，虽然测试用例的执行、管理、统计比较方便，但依然存在编写用例效率不高、思路不够发散、在产品快速迭代过程中比较耗时等问题...
- 3、公司自研测试管理工具，这是个不错的选择，但对于大部分小公司、小团队来说，一方面研发维护成本高，另一方面对技术要有一定要求...
- 4、...


基于这些情况，现在越来越多公司选择使用**思维导图**这种高效的生产力工具进行用例设计，特别是敏捷开发团队。

事实上也证明，思维导图其发散性思维、图形化思维的特点，跟测试用例设计时所需的思维非常吻合，所以在实际工作中极大提升了我们测试用例设计的效率，也非常方便测试用例评审。

但是与此同时，使用思维导图进行测试用例设计的过程中也带来不少问题：
- 1、测试用例难以量化管理、执行情况难以统计；
- 2、测试用例执行结果与BUG管理系统难以打通；
- 3、团队成员用思维导图设计用例的风格各异，沟通成本巨大；
- 4、...

综合以上情况，我们可以发现不同的测试用例设计方式，各有各个的优劣。

那么问题来了，我们能不能将它们各自优点合在一起呢？这样不就可以提升我们的效率了！

于是，这时候 **XMind2TestCase** 就应运而生了，该工具基于 Python 实现，通过制定**测试用例通用模板**，
然后使用 **[XMind](https://www.xmind.cn/)** 这款广为流传且开源的思维导图工具进行用例设计。
其中制定**测试用例通用模板**是一个非常核心的步骤（具体请看[使用指南](https://github.com/zhuifengshen/xmind2testcase/blob/master/webtool/static/guide/index.md)），有了通用的测试用例模板，我们就可以在 XMind 文件上解析并提取出测试用例所需的基本信息，
然后合成常见**测试用例管理系统**所需的**用例导入文件**。这样就将 **XMind 设计测试用例的便利**与**常见测试用例系统的高效管理**结合起来了！

当前 **XMind2TestCase** 已实现从 XMind 文件到 TestLink 和 Zentao(禅道) 两大常见用例管理系统的测试用例转换，同时也提供 XMind 文件解析后的两种数据接口
（TestSuites、TestCases两种级别的JSON数据），方便快速与其他测试用例管理系统打通。
