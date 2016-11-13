    

server {

    listen 80;
    server_name .aychedee.com;

    root /srv/www/www.aychedee.com/_build/;
    index index.html;

    location /static {

        alias /srv/www/www.aychedee.com/static/;
        access_log off;
        autoindex on;

    }

    location /p {

        alias /srv/www/www.aychedee.com/_presentations/;
        autoindex on;

    }

    location /page {

        alias /srv/www/www.aychedee.com/_build/page/;
        autoindex on;

    }

    location /feed.xml { 

        alias /srv/www/www.aychedee.com/_build/feed.atom;
        access_log off;
    }

    location /favicon.ico { 

        alias /srv/www/www.aychedee.com/static/favicon.ico;
        access_log off;
    }

    location /robots.txt { 

        alias /srv/www/www.aychedee.com/static/robots.txt;
        access_log off;
    }

    location /entries.csv {

        auth_basic " You will need to enter a password ";
        auth_basic_user_file htpasswd;
        alias /home/hansel/bizzl/entries.csv;
    }

    #location /ewan {

    #    alias /home/hansel/Downloads;
    #    autoindex on;
    #}

    access_log /var/log/nginx/www.aychedee.com.access.log;
    error_log /var/log/nginx/www.aychedee.com.error.log;	

}
