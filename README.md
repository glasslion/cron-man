# cron-man

私の定时任务

这个仓库用于集中管理我个人用的一些需要定时执行的自动化脚本。

这些脚本比较轻量，运行时长很短，频率也低， 如果为其单独配置服务器，不仅浪费资源， 也徒增运维成本。 因此我通过 CircleCI 来实现定时执行的功能。 由于CircleCI 的配置文件格式比较复杂，本项目通过 ` scripts/converter.py` 脚本 来将 crontab 自动转为 CircleCI 的配置文件。



格式和标准的 crontab 格式 相同， 只是在每行的末尾需要 在 @@ @@ 之间填入 job name。
```
30 12 * * * python xxxxx.py  @@job_name@@
```
