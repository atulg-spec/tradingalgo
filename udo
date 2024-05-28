[0;1;31mWarning:[0m The unit file, source configuration file or drop-ins of gunicorn.service changed on disk. Run 'systemctl daemon-reload' to reload units.
[0;1;32m●[0m gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; enabled; vendor preset: enabled)
     Active: [0;1;32mactive (running)[0m since Thu 2024-05-02 04:48:20 CEST; 12h ago
TriggeredBy: [0;1;32m●[0m gunicorn.socket
   Main PID: 530 (gunicorn)
      Tasks: 13 (limit: 9439)
     Memory: 219.6M
        CPU: 14.640s
     CGroup: /system.slice/gunicorn.service
             ├─530 /root/trading/env/bin/python /root/trading/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/root/trading/trading.sock trading.wsgi:application
             ├─639 /root/trading/env/bin/python /root/trading/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/root/trading/trading.sock trading.wsgi:application
             ├─642 /root/trading/env/bin/python /root/trading/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/root/trading/trading.sock trading.wsgi:application
             └─643 /root/trading/env/bin/python /root/trading/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/root/trading/trading.sock trading.wsgi:application

May 02 04:48:20 vmi1524585.contaboserver.net systemd[1]: Started gunicorn daemon.
May 02 04:48:20 vmi1524585.contaboserver.net gunicorn[530]: [2024-05-02 04:48:20 +0200] [530] [INFO] Starting gunicorn 21.2.0
May 02 04:48:20 vmi1524585.contaboserver.net gunicorn[530]: [2024-05-02 04:48:20 +0200] [530] [INFO] Listening at: unix:/run/gunicorn.sock (530)
May 02 04:48:20 vmi1524585.contaboserver.net gunicorn[530]: [2024-05-02 04:48:20 +0200] [530] [INFO] Using worker: sync
May 02 04:48:20 vmi1524585.contaboserver.net gunicorn[639]: [2024-05-02 04:48:20 +0200] [639] [INFO] Booting worker with pid: 639
May 02 04:48:20 vmi1524585.contaboserver.net gunicorn[642]: [2024-05-02 04:48:20 +0200] [642] [INFO] Booting worker with pid: 642
May 02 04:48:20 vmi1524585.contaboserver.net gunicorn[643]: [2024-05-02 04:48:20 +0200] [643] [INFO] Booting worker with pid: 643
