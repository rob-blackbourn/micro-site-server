# micro-site-server

An example micro site/server architecture

# Config

## nginx

```bash
        location /micro-site/auth {
                proxy_pass http://localhost:10201;
        }

        location /micro-site/navigator/api {
                proxy_pass http://localhost:10202;
        }

        location /micro-site/site1/api {
                proxy_pass http://localhost:10203;
        }

        location /micro-site/site2/api {
                proxy_pass http://localhost:10204;
        }

        location /micro-site/site1/ui {
                proxy_pass http://localhost:10301;
        }

        location /micro-site/site2/ui {
                proxy_pass http://localhost:10302;
        }

```
