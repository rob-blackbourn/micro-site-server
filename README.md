# micro-site-server

An example micro site/server architecture

# Config


# Chrome

See here: https://stackoverflow.com/questions/50788043/how-to-trust-self-signed-localhost-certificates-on-linux-chrome-and-firefox
And here: https://fabianlee.org/2018/02/17/ubuntu-creating-a-trusted-ca-and-san-certificate-using-openssl-on-ubuntu/

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
