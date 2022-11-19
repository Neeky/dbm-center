[toc]

---


## API 列表

---

### /apis/agents

|**路径**|**请求方式**|**功能**|**返回值**|**明细**|
|-------|-----------|-------|----------|--------|
|/apis/agents/|**POST**|实现 agent 的注册功能| {id:xxx, message:''}|**id**  agent 注册之后得到的唯一键. **message** 其它说明信息，没有异常的情况下是空串|
|/apis/agents/|**GET**|检查 dbm-center 所有的 agent 信息| {agents:[], message:''}| |
|/apis/agents/pk:int|**GET**|查询单个 agent 的信息|
|/apis/agents/pk:int|**PUT**|更新心跳|{pk:int, message:''}|