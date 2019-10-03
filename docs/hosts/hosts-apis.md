## 目录
- [hosts概要](#hosts概要)
- [hostsAPI说明](#hostsAPI说明)
- [hosts/idcs/add](#hosts/idcs/add)
---


## hosts概要
   **hosts目标是完成对主机相关功能的自动化**

   ---
   

## hostsAPI说明
|**名称**|**接口**|**http方法**|
|--------|-------|-----------|
|增加新的IDC机房| /hosts/idcs/add | post|
|更新给定的IDC机房信息| /hosts/idcs/{id}/update | post|
|查询给定的IDC机房信息| /hosts/idcs/{id} | get|
|查询所有的IDC机房信息| /hosts/idcs | get|

---


## hosts/idcs/add
   **实现添加 IDC 机房的功能**
   ```python
   ```