"""

$$$$$$$\                                          $$ \
$$  __$$\                                         $$ |
$$ |  $$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  $$ |
$$$$$$$  |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$ |
$$  ____/ $$ |  \__|$$ /  $$ |$$ /  $$ |$$$$$$$$ |$$ |
$$ |      $$ |      $$ |  $$ |$$ |  $$ |$$   ____|$$ |
$$ |      $$ |      \$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |
\__|      \__|       \______/ $$  ____/  \_______|\__|
                              $$ |
                              $$ |
                              \__|

"""



import argparse
import datetime
import getpass
import multiprocessing
import os
import platform
import random
import shutil
import socket
import subprocess
import sys

from __about__ import *

try:
    import yaml
except ImportError as ex:
    print("PyYaml is missing. pip install pyyaml")
try:
    from jinja2 import Template
except ImportError as ex:
    print("Jinja2 is missing. pip install jinja2")


PY_EXECUTABLE = sys.executable
PY_USER = getpass.getuser()
CWD = os.getcwd()

NGINX_DEFAULT_PORT = 80
GUNICORN_PORT_RANGE = [8000, 9000]  # Port range for gunicorn proxy
GUNICORN_DEFAULT_THREADS = 4
GUNICORN_DEFAULT_MAX_REQUESTS = 500
GUNICORN_DEFAULT_WORKER_CLASS = "gevent"

VIRTUALENV = None
VERBOSE = False
VIRTUALENV_DIRECTORY = "/root/.virtualenvs"
VIRTUALENV_DEFAULT_PACKAGES = ["gunicorn", "gevent"]
LOCAL_BIN = "/usr/local/bin"

DEPLOY_CONFIG_FILE = "propel.yml"
DEPLOY_CONFIG = None

# Configuration per distribution
DIST_CONF = {
    "RHEL": {
        "NGINX_CONF_FILE": "/etc/nginx/conf.d/%s.conf",
        "APT_GET": "yum",
        "INSTALL_PROGRAMS": ["nginx", 'groupinstall "Development Tools"', "python-devel", "php-fpm", "supervisor"],
        "RELOAD_PROGRAMS": ["nginx", "php-fpm"],
        "SERVICES": ["supervisor", "nginx", "php-fpm"],
        "UPSTART_CMD": "chkconfig %s on"
    },
    "DEBIAN": {
        "NGINX_CONF_FILE": "/etc/nginx/sites-enabled/%s.conf",
        "APT_GET": "apt-get",
        "INSTALL_PROGRAMS": ["nginx", 'python-dev', "php5-fpm", "supervisor"],
        "RELOAD_PROGRAMS": ["nginx", "php5-fpm"],
        "SERVICES": ["supervisor", "nginx", "php5-fpm"],
        "UPSTART_CMD": "sudo update-rc.d %s defaults"
    }
}

# ------------------------------------------------------------------------------

# SUPERVISOR
SUPERVISOR_CTL = "supervisorctl"
SUPERVISOR_LOG_DIR = "/var/log/supervisor"
SUPERVISOR_CONF_DIR = "/etc/supervisor/conf.d"
SUPERVISOR_TPL = """
[program:{name}]
command={command}
directory={directory}
user={user}
autostart=true
autorestart=true
stopwaitsecs=600
startsecs=10
stdout_logfile={log}
stderr_logfile={log}
environment={environment}
"""

NGINX_CONFIG = """
{%- macro SET_PATH(directory, path="") %}
    {%- if path and path.startswith('/') -%}
        {{ path }}
    {%- else -%}
        {{ directory }}/{{ path }}
    {%- endif -%}
{% endmacro -%}


server {
    listen {{ PORT }};
    server_name {{ SERVER_NAME }};
    root {{ SET_PATH(DIRECTORY, ROOT_DIR) }};

    {% if LOGS_DIR %}
    access_log {{ LOGS_DIR }}/access_{{ SERVER_NAME }}.log;
    error_log {{ LOGS_DIR }}/error_{{ SERVER_NAME }}.log;
    {% endif %}

{%- if SSL_DIRECTIVES %}

    {{ SSL_DIRECTIVES }}

{%- elif SSL_CERT and SSL_KEY %}

    if ($scheme = "http") {
        return 301 https://{{ SERVER_NAME }}$request_uri;
    }

    listen 443 ssl;
    ssl_certificate     {{ SET_PATH(DIRECTORY, SSL_CERT) }} ;
    ssl_certificate_key {{ SET_PATH(DIRECTORY, SSL_KEY) }} ;

    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout  5m;
    ssl_ciphers  HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers   on;

{% endif -%}


{% if MAINTENANCE["ACTIVE"] %}
    set $maintenance on;

    {% set maintenance_page = "maintenance.html" %}
    {% if MAINTENANCE["PAGE"] %}
        {% set maintenance_page =  MAINTENANCE["PAGE"] %}
    {% endif %}

    # allow ips
    {% if MAINTENANCE["ALLOW_IPS"] %}
        if ($remote_addr ~ ({{ MAINTENANCE["ALLOW_IPS"] | join("|") }})) {
            set $maintenance off;
        }
    {% endif %}

    if ($maintenance = on) {
        return 503;
    }

    error_page 503 @maintenance;
    location @maintenance {
        {% if not MAINTENANCE["PAGE"] %}
            root /var/propel;
        {% endif %}

         rewrite ^(.*)$ /{{ maintenance_page }} break;
    }
{% endif %}


{% if (not MAINTENANCE["ACTIVE"])  or (MAINTENANCE["ACTIVE"] and MAINTENANCE["ALLOW_IPS"]) %}
    {% if PROXY_PORT %}
        location / {
            proxy_pass http://127.0.0.1:{{ PROXY_PORT }}/;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $server_name;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

    {% else %}

        location / {
            index index.html index.htm index.php;
        }

        # Pass PHP scripts to PHP-FPM
        location ~* \.php$ {
            fastcgi_index   index.php;
            fastcgi_pass    127.0.0.1:9000;
            include         fastcgi_params;
            fastcgi_param   SCRIPT_FILENAME    $document_root$fastcgi_script_name;
            fastcgi_param   SCRIPT_NAME        $fastcgi_script_name;
        }

    {% endif %}

{% else %}

    location / {
        return 503;
    }

{% endif %}


{%- if ALIASES %}
    {%- for alias, location in ALIASES.items() %}
    location {{ alias }} {
        alias {{ SET_PATH(DIRECTORY, location) }} ;
    }
    {% endfor -%}
{% endif -%}

    {{ SERVER_DIRECTIVES }}
}

{% if FORCE_NON_WWW or FORCE_WWW %}

server {
    listen {{ PORT }};

    {% if SSL_CERT and SSL_KEY %}
    listen 443 ssl;
    {% endif %}

    {% if FORCE_NON_WWW %}

        server_name www.{{ NAME }};
        return 301 $scheme://$host$request_uri;

    {% elif FORCE_WWW and not NAME.startswith('www.') %}

        server_name {{ NAME }};
        return 301 $scheme://www.{{ NAME }}$request_uri;

    {% endif %}
}

{% endif %}

"""

POST_RECEIVE_HOOK_CONFIG = """
#!/bin/sh
while read oldrev newrev refname
do
    branch=$(git rev-parse --symbolic --abbrev-ref $refname)
    if [ "master" = "$branch" ]; then
        GIT_WORK_TREE={{ WORKING_DIR }} git checkout -f
        cd {{ WORKING_DIR }}
        {{ COMMAND }}
    fi
done
"""

# ------------------------------------------------------------------------------
def _print(text):
    """
    Verbose print. Will print only if VERBOSE is ON
    """
    if VERBOSE:
        print(text)

def run(cmd, verbose=True):
    """ Shortcut to subprocess.call """
    if verbose and VERBOSE:
        subprocess.call(cmd.strip(), shell=True)
    else:
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process.communicate()[0]

def runvenv(command, virtualenv=None):
    """
    run with virtualenv with the help of .bashrc
    :params command:
    :params  virtualenv: The venv name
    """
    kwargs = dict()
    if not VERBOSE:
        kwargs = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if virtualenv:
        command = "workon %s; %s; deactivate" % (virtualenv, command)
    cmd = ["/bin/bash", "-i", "-c", command]
    process = subprocess.Popen(cmd, **kwargs)
    return process.communicate()[0]

def get_venv_bin(bin_program=None, virtualenv=None):
    """
    Get the bin path of a virtualenv program
    """
    bin = (VIRTUALENV_DIRECTORY + "/%s/bin") % virtualenv if virtualenv else LOCAL_BIN
    return (bin + "/%s") % bin_program if bin_program else bin

def is_port_open(port, host="127.0.0.1"):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except Exception as e:
        return False

def generate_random_port():
    while True:
        port = random.randrange(GUNICORN_PORT_RANGE[0], GUNICORN_PORT_RANGE[1])
        if not is_port_open(port):
            return port

def get_dist():
    """
    Return the running distribution group
    RHEL: RHEL, CENTOS, FEDORA
    DEBIAN: UBUNTU, DEBIAN
    """
    dist_name = platform.linux_distribution()[0]
    system_name = platform.system()

    if dist_name.upper() in ["RHEL", "CENTOS", "FEDORA"]:
        return "RHEL"
    elif dist_name.upper() in ["DEBIAN", "UBUNTU"]:
        return "DEBIAN"
    raise NotImplemented("Platform '%s' is not compatible with Propel" % dist_name)

def get_dist_config(key):
    """
    Return the
    """
    dist = get_dist()
    if dist in DIST_CONF:
        return DIST_CONF[dist].get(key)
    raise AttributeError("Dist config '%s' not found" % key)

def reload_services():
    for svc in get_dist_config("RELOAD_PROGRAMS"):
        run("sudo service %s reload" % svc)

def get_domain_conf_file(domain):
    return get_dist_config("NGINX_CONF_FILE") % domain

# VirtualenvWrapper
def virtualenv_make(name):
    runvenv("mkvirtualenv %s" % name)
    pip = get_venv_bin(bin_program="pip", virtualenv=name)
    packages = " ".join([p for p in VIRTUALENV_DEFAULT_PACKAGES])
    runvenv("%s install %s" % (pip, packages), virtualenv=name)

def virtualenv_remove(name):
    runvenv("rmvirtualenv %s" % name)

# Deployment
def get_deploy_config(directory):
    """
    Return dict of the yaml file
    :params directory:
    """
    global DEPLOY_CONFIG

    if not DEPLOY_CONFIG:
        yaml_file = directory + "/" + DEPLOY_CONFIG_FILE
        if not os.path.isfile(yaml_file):
            raise Exception("Propel file '%s' is missing" % yaml_file)
        with open(yaml_file) as jfile:
            DEPLOY_CONFIG = yaml.load(jfile)
    return DEPLOY_CONFIG

def _parse_command(command, virtualenv=None, directory=None):
    command = command.replace("$PYTHON_ENV", get_venv_bin(bin_program="python", virtualenv=virtualenv))
    command = command.replace("$LOCAL_BIN", get_venv_bin(virtualenv=virtualenv))
    command = command.replace("$CWD", directory)
    return command

def reload_server():
    reload_services()
    Supervisor.reload()

class Supervisor(object):
    """
    Supervisor Class
    """

    @classmethod
    def ctl(cls, action, name):
        return run("%s %s %s" % (SUPERVISOR_CTL, action, name))

    @classmethod
    def status(cls, name):
        status = run("%s %s %s" % (SUPERVISOR_CTL, "status", name), verbose=False)
        if status:
            _status = ' '.join(status.split()).split(" ")
            if _status[0] == name:
                return _status[1]
        return None

    @classmethod
    def list_status(cls):
        statuses = []
        _ = run("%s %s %s" % (SUPERVISOR_CTL, "status", ""), verbose=False)
        for line in _.split("\n"):
            _status = ' '.join(line.split()).split(" ")
            name = _status[0]
            if "propel-" in name:
                statuses.append(line)
        return statuses

    @classmethod
    def start(cls, name, command, directory="/", user="root", environment=None):
        """
        To Start/Set  a program with supervisor
        :params name: The name of the program
        :param command: The full command
        :param directory: The directory
        :param user:
        :param environment:
        """
        log_file = "%s/%s.log" % (SUPERVISOR_LOG_DIR, name)
        conf_file = "%s/%s.conf" % (SUPERVISOR_CONF_DIR, name)
        if cls.status(name) == "RUNNING":
            cls.ctl("stop", name)
        with open(conf_file, "wb") as f:
            f.write(SUPERVISOR_TPL.format(name=name,
                                          command=command,
                                          log=log_file,
                                          directory=directory,
                                          user=user,
                                          environment=environment or ""))
        cls.reload()
        cls.ctl("start", name)

    @classmethod
    def stop(cls, name, remove=True):
        """
        To Stop/Remove a program
        :params name: The name of the program
        :remove: If True will also delete the conf file
        """
        conf_file = "%s/%s.conf" % (SUPERVISOR_CONF_DIR, name)
        cls.ctl("stop", name)
        if remove:
            if os.path.isfile(conf_file):
                os.remove(conf_file)
            cls.ctl("remove", name)
        cls.reload()

    @classmethod
    def reload(cls):
        """
        Reload supervisor with the changes
        """
        cls.ctl("reread", "")
        cls.ctl("update", "")

    @classmethod
    def restart(cls):
        """
        To restart supervisor
        """
        cls.ctl("restart", "all")

class Git(object):
    def __init__(self, directory):
        self.directory = directory

    def get_working_dir(self, repo):
        working_dir = "%s/%s" % (self.directory, repo)
        bare_repo = "%s.git" % working_dir
        return working_dir, bare_repo

    def init_bare_repo(self, repo):
        working_dir, bare_repo = self.get_working_dir(repo)
        logs_dir = "%s.logs" % working_dir

        if not os.path.isdir(logs_dir):
            os.makedirs(logs_dir)
        if not os.path.isdir(working_dir):
            os.makedirs(working_dir)
        if not os.path.isdir(bare_repo):
            os.makedirs(bare_repo)
            run("cd %s && git init --bare" % bare_repo)
            return True
        return False

    def update_post_receive_hook(self, repo, command=""):
        working_dir, bare_repo = self.get_working_dir(repo)
        post_receice_hook_file = "%s/hooks/post-receive" % bare_repo

        # Always make a backup of the post receive hook
        if os.path.isfile(post_receice_hook_file):
            ts = datetime.datetime.now().strftime("%s")
            backup_file = (post_receice_hook_file + "-bk-%s") % ts
            shutil.copyfile(post_receice_hook_file, backup_file)

        with open(post_receice_hook_file, "wb") as f:
            content = Template(POST_RECEIVE_HOOK_CONFIG)\
                .render(WORKING_DIR=working_dir, COMMAND=command)
            f.write(content)
        run("chmod +x %s " % post_receice_hook_file)

class App(object):
    virtualenv = None
    directory = None
    deployed_info = []

    def __init__(self, directory):
        self.config = get_deploy_config(directory)
        self.directory = directory
        self.virtualenv = self.config["virtualenv"] if "virtualenv" in self.config else {}

    def get_web_by_name(self, name):
        if "web" in self.config:
            for _ in self.config["web"]:
                if _.get("name") == name:
                    return _

    def publish_web(self, name=None, undeploy=False, maintenance=False, site=None):
        """

        """

        # Maintenance
        _maintenance = {"active": False, "page": None, "allow_ips": []}
        if "maintenance" in self.config:
            _maintenance.update(self.config["maintenance"])
        elif maintenance:
            _maintenance.update({"active": True})

        if not site:
            site = self.get_web_by_name(name)

        if not site:
            raise ValueError("Site '%s' doesn't exist" % name)

        if "application" in site and not self.virtualenv.get("name"):
            raise TypeError("'virtualenv' is missing for Python web/app")

        name = site.get("name")
        directory = self.directory
        nginx = site.get("nginx", {})
        gunicorn_options = site.get("gunicorn", {})
        application = site.get("application", None)
        environment = site.get("environment", None)
        user = site.get("user", "root")
        remove = site.get("remove", False)
        exclude = site.get("exclude", False)
        gunicorn_app_name = "propel-web__%s" % name
        nginx_config_file = get_domain_conf_file(name)
        proxy_port = None

        # Exclude from re/deploying
        if exclude:
            return

        if remove or undeploy:
            if os.path.isfile(nginx_config_file):
                os.remove(nginx_config_file)
            if application:
                Supervisor.stop(name=gunicorn_app_name, remove=True)
            return

        # Python app will use Gunicorn+Gevent and Supervisor
        if application:
            proxy_port = generate_random_port()
            default_gunicorn = {
                "workers": (multiprocessing.cpu_count() * 2) + 1,
                "threads": GUNICORN_DEFAULT_THREADS,
                "max-requests": GUNICORN_DEFAULT_MAX_REQUESTS,
                "worker-class": GUNICORN_DEFAULT_WORKER_CLASS
            }
            [gunicorn_options.setdefault(k, v) for k, v in
             default_gunicorn.items()]
            settings = " ".join(["--%s %s" % (x[0], x[1]) for x in
                                 gunicorn_options.items()])
            gunicorn_bin = get_venv_bin(bin_program="gunicorn",
                                        virtualenv=self.virtualenv.get("name"))

            command = "{GUNICORN_BIN} -b 0.0.0.0:{PROXY_PORT} {APP} {SETTINGS}" \
                .format(GUNICORN_BIN=gunicorn_bin,
                        PROXY_PORT=proxy_port,
                        APP=application,
                        SETTINGS=settings, )

            Supervisor.start(name=gunicorn_app_name,
                             command=command,
                             directory=directory,
                             user=user,
                             environment=environment)

        logs_dir = nginx.get("logs_dir", None)
        if not logs_dir:
            logs_dir = "%s.logs" % self.directory
            if not os.path.isdir(logs_dir):
                os.makedirs(logs_dir)

        self.deployed_info.append((name, proxy_port, gunicorn_app_name))

        with open(nginx_config_file, "wb") as f:
            context = dict(NAME=name,
                           SERVER_NAME=nginx.get("server_name", name),
                           DIRECTORY=directory,
                           PROXY_PORT=proxy_port,
                           PORT=nginx.get("port", NGINX_DEFAULT_PORT),
                           ROOT_DIR=nginx.get("root_dir", ""),
                           ALIASES=nginx.get("aliases", {}),
                           FORCE_NON_WWW=nginx.get("force_non_www", True),
                           FORCE_WWW=nginx.get("force_www", False),
                           SERVER_DIRECTIVES=nginx.get("server_directives", ""),
                           SSL_CERT=nginx.get("ssl_cert", ""),
                           SSL_KEY=nginx.get("ssl_key", ""),
                           SSL_DIRECTIVES=nginx.get("ssl_directives", ""),
                           LOGS_DIR=logs_dir,
                           MAINTENANCE={}
                           )
            content = Template(NGINX_CONFIG).render(**context)
            f.write(content)

    def deploy_web(self, undeploy=False, maintenance=False):
        """
        To deploy/undeploy web app/sites
        """

        # Maintenance
        _maintenance = {"active": False, "page": None, "allow_ips": []}
        if "maintenance" in self.config:
            _maintenance.update(self.config["maintenance"])
        elif maintenance:
            _maintenance.update({"active": True})

        if "web" in self.config:
            for site in self.config["web"]:
                if "name" not in site:
                    raise TypeError("'name' is missing in sites config")
                if "application" in site and not self.virtualenv.get("name"):
                    raise TypeError("'virtualenv' is missing for Python web/app")
                self.publish_web(site=site)
        else:
            raise TypeError("'web' is missing in propel.yml")

    def maintenance(self, names=[], is_on=True, undeploy_all=False):
        """
        Will put all the sites under maintenance
        To maintenance off, just deploy_web
        """
        if not is_on:
            self.deploy_web()
        elif undeploy_all:
            self.deploy_web(maintenance=True)
            self.run_workers(undeploy=True)
        else:
            for name in names:
                self._maintenance(name)

    def _maintenance(self, name):
        """
        Will put all the sites under maintenance
        To maintenance off, just deploy_web
        """
        site = self.get_web_by_name(name)
        if not site:
            raise ValueError("Site '%s' doesn't exist" % name)

        name = site["name"]
        nginx = site["nginx"] if "nginx" in site else {}
        directory = self.directory
        nginx_config_file = get_domain_conf_file(name)
        maintenance = {"active": False, "page": None, "allow_ips": []}

        with open(nginx_config_file, "wb") as f:
            context = dict(NAME=name,
                           SERVER_NAME=nginx.get("server_name", name),
                           DIRECTORY=directory,
                           PROXY_PORT=None,
                           PORT=nginx.get("port", NGINX_DEFAULT_PORT),
                           ROOT_DIR=nginx.get("root_dir", ""),
                           ALIASES=nginx.get("aliases", {}),
                           FORCE_NON_WWW=nginx.get("force_non_www", False),
                           FORCE_WWW=nginx.get("force_www", False),
                           SERVER_DIRECTIVES=nginx.get("server_directives", ""),
                           SSL_CERT=nginx.get("ssl_cert", ""),
                           SSL_KEY=nginx.get("ssl_key", ""),
                           SSL_DIRECTIVES=nginx.get("ssl_directives", ""),
                           MAINTENANCE={"ACTIVE": True,
                                        "PAGE": maintenance.get("page", None),
                                        "ALLOW_IPS": []}
                           )
            content = Template(NGINX_CONFIG).render(**context)
            f.write(content)

    def run_scripts(self, name):
        """
        Run a one time script
        :params script_name: (string) The script name to run.
        """
        if "scripts" in self.config and name in self.config["scripts"]:
            for script in self.config["scripts"][name]:
                if "command" not in script:
                    raise TypeError("'command' is missing in scripts")

                # Exclude from running
                exclude = script.get("exclude", False)
                if exclude:
                    continue

                directory = script.get("directory", self.directory)
                command = _parse_command(command=script["command"],
                                         virtualenv=self.virtualenv.get("name"),
                                         directory=directory)
                runvenv("cd %s; %s" % (directory, command), virtualenv=self.virtualenv.get("name"))

    def run_workers(self, name=None, undeploy=False):

        if "workers" in self.config:
            if undeploy and name is None:
                workers = [v for _, v in self.config["workers"].items()]
            else:
                if name in self.config["workers"]:
                    workers = self.config["workers"][name]
                else:
                    raise TypeError("Missing worker: %s" % name)

            for worker in workers:
                if "name" not in worker:
                    raise TypeError("'name' is missing in workers")
                if "command" not in worker:
                    raise TypeError("'command' is missing in workers")

                name = "propel-worker__%s" % worker.get("name")
                user = worker.get("user", "root")
                environment = worker.get("environment", "")
                directory = worker.get("directory", self.directory)
                command = _parse_command(command=worker["command"],
                                         virtualenv=self.virtualenv.get("name"),
                                         directory=directory)
                remove = worker.get("remove", False)
                exclude = worker.get("exclude", False)

                if exclude:  # Exclude worker from re/running
                    continue

                if remove or undeploy:
                    Supervisor.stop(name=name, remove=True)
                    continue

                Supervisor.start(name=name,
                                 command=command,
                                 directory=directory,
                                 user=user,
                                 environment=environment)

    def install_requirements(self, pip_options=None):
        requirements_file = self.directory + "/requirements.txt"
        if os.path.isfile(requirements_file):
            pip = get_venv_bin(bin_program="pip",
                               virtualenv=self.virtualenv.get("name"))
            pip_options = pip_options or ""
            runvenv("%s install -r %s %s" % (pip, requirements_file, pip_options),
                    virtualenv=self.virtualenv.get("name"))

    def setup_virtualenv(self):

        if self.virtualenv.get("name"):
            if self.virtualenv.get("rebuild") == True:
                self.destroy_virtualenv()
            if not self.has_virtualenv():
                virtualenv_make(self.virtualenv.get("name"))

    def destroy_virtualenv(self):
        if self.virtualenv.get("name"):
            virtualenv_remove(self.virtualenv.get("name"))

    def has_virtualenv(self):
        if self.virtualenv.get("name"):
            path = "%s/%s" % (VIRTUALENV_DIRECTORY, self.virtualenv.get("name"))
            return os.path.isdir(path)
        return False

def print_logo():
    _print(__doc__)

def cmd():
    global CWD

    try:
        global VIRTUALENV_DIRECTORY
        global VERBOSE



        parser = argparse.ArgumentParser(description="%s %s" % (__title__, __version__))
        parser.add_argument("-w", "--webs", help="Deploy sites by name. ie [-w abc.com xyz.com ...]", nargs='*')
        parser.add_argument("--all-webs", help="Deploy all sites", action="store_true")
        parser.add_argument("-s", "--scripts", help="Run script by specifying name:"
                                                    " ie: [-s pre_web post_web other_one]", nargs='*')
        parser.add_argument("-k", "--workers", help="Run Workers by specifying name: ie [-k tasks othertasks]", nargs='*')
        parser.add_argument("-r", "--reload", help="To refresh the servers", action="store_true")
        parser.add_argument("-x", "--undeploy", help="To UNDEPLOY the application", action="store_true")
        parser.add_argument("-m", "--maintenance", help="Values: on|off - To set the site on maintenance. ie [--maintenance on]")
        parser.add_argument("-c", "--create", help="Create a new application repository, set the git init for web push")
        parser.add_argument("--basedir", help="The base directory when creating a new application. By default it's /home")
        parser.add_argument("--silent", help="Disable verbosity", action="store_true")
        parser.add_argument("--status",  help="Show all the Propel statuses", action="store_true")
        parser.add_argument("--restart",  help="Restart all managed Supervisor processes", action="store_true")

        parser.add_argument("--git-init", help="Setup a git bare repo $name to push content to. [--git-init $name]")
        parser.add_argument("--git-push-web", help="Set propel to deploy automatically when "
                                                   "push to the bare repo. [--git-push-web $name]")
        parser.add_argument("--git-push-cmd", help="Setup Command to execute after git push. Put cmds within quotes"
                                                   "ie: [--git-push-cmd $name 'ls  -l' 'cd ']", nargs='*')
        parser.add_argument("--debug", help="To output the full error stack in", action="store_true")
        arg = parser.parse_args()
        VERBOSE = False if arg.silent else True

        _print("")
        _print("-" * 80)
        print_logo()
        _print(__version__)
        _print("-" * 80)
        _print("")

        # Supervisor test
        if not os.path.isdir(SUPERVISOR_CONF_DIR):
            print("PROPEL has not been setup yet.")
            print("Run propel-setup")
            print("")
            exit()

        # Show processes
        if arg.status:
            print("::: STATUS :::\n")
            statuses = Supervisor.list_status()
            print("\n".join(statuses))
            print("")
            exit()

        if arg.create:
            basedir = "/home"
            if arg.basedir:
                basedir = arg.basedir
            projectname = arg.create.lower()

            _print("==== CREATE NEW REPOSITORY : %s \n" % projectname)

            if not os.path.isdir(basedir):
                raise IOError("Base directory: '%s' doesn't exist")

            CWD = basedir
            project_dir = "%s/%s" % (CWD, projectname)
            arg.git_init = projectname
            arg.git_push_web = projectname
            arg.maintenance = False
            arg.undeploy = False
            arg.websites = False
            arg.scripts = False
            arg.workers = False

            if not os.path.exists(project_dir):
                os.makedirs(project_dir)

        git = Git(CWD)
        app = None

        # Maintenance
        if arg.maintenance:
            app = App(CWD)
            maintenance = arg.maintenance.upper()
            if maintenance == "ON":
                _print("::: MAINTENANCE PAGE ON :::")
                app.maintenance()
            elif maintenance == "OFF":
                _print("::: MAINTENANCE PAGE OFF :::")
                arg.websites = True

        # Undeploy
        if arg.undeploy:
            _print("::: UNDEPLOY :::")
            app = App(CWD)
            app.deploy_web(undeploy=True)
            app.run_workers(undeploy=True)
            app.run_scripts("undeploy")
            app.destroy_virtualenv()

        if arg.restart:
            _print("==== Restarting all processes...")
            Supervisor.restart()

        # Deploy: Websites, scripts, workers may require a virtualenv
        elif arg.webs or arg.all_webs or arg.scripts or arg.workers:
            app = App(CWD)

            # Global maintenance - maintenance["active"]= True only, ips must be empty
            _m = app.config.get("maintenance")
            if _m and _m.get("active") is True and not _m.get("allow_ips"):
                app.maintenance(names=arg.webs, undeploy_all=True)
                _print("::: GLOBAL MAINTENANCE :::")
                _print("")
                exit()

            # MAINTENACE Auto maintenance before doing any web deployment
            if arg.webs or arg.all_webs:
                _print("=== Setup maintenance ...")
                app.maintenance(names=arg.webs)

            # Virtualenv
            if app.virtualenv.get("name"):
                _print("::: SETTING UP VIRTUALENV :::")
                _print("==== Virtualenv: %s " %  app.virtualenv.get("name"))
                app.setup_virtualenv()

                # Disabled, need to match the path that should be set during setup
                # if app.virtualenv.get("directory"):
                #     VIRTUALENV_DIRECTORY = app.virtualenv.get("directory")
                #

                _print("::: INSTALLING REQUIREMENTS :::")
                pip_options = app.virtualenv.get("pip_options", "")
                app.install_requirements(pip_options)

            _print("==== Running script: 'before_all' ...")
            app.run_scripts("before_all")

            # Scripts. Scripts must run before web or working, as they may contain
            # necessary commands

            if arg.scripts:
                _print("::: RUN SCRIPTS :::")
                for name in arg.scripts:
                    _print("====  Scripts: %s ..." % name)
                    app.run_scripts(name)

            # Web
            if arg.webs or arg.all_webs:
                _print("::: DEPLOY WEBSITES :::")

                _print("==== Running script: 'before_web' ...")
                app.run_scripts("before_web")

                if arg.webs:
                    for name in arg.webs:
                        _print("==== Deploying site: %s ... " % name)
                        app.publish_web(name=name)
                else:
                    _print("==== Deploying ALL WEBS ... ")
                    app.deploy_web()

                _print("==== Running script: 'after_web' ...")
                app.run_scripts("after_web")

            # Workers
            if arg.workers:
                _print("::: RUN WORKERS :::")

                _print("==== Running script: 'before_workers' ...")
                app.run_scripts("before_workers")

                for name in arg.workers:
                    _print("==== Worker: '%s' ..." % name)
                    app.run_workers(name)

                _print("==== Running script: 'after_workers' ...")
                app.run_scripts("after_workers")

            _print("==== Running script: 'after_all' ...")
            app.run_scripts("after_all")

            if arg.webs or arg.all_webs:
                _print("==== Reloading NGINX ...")
                reload_server()


        # Extra
        else:
            if arg.git_init:
                repo = arg.git_init
                bare_repo = "%s/%s.git" % (CWD, repo)
                directory = "%s/%s" % (CWD, repo)
                _print(":: GIT INIT BARE REPO ::")
                if git.init_bare_repo(repo):
                    git.update_post_receive_hook(repo, False)
                _print("\n\t Git Repository: %s" % bare_repo)
                _print("\n\t Content Directory: %s/" % directory)
                _print("\n\t Add to git remote:")
                _print("\t\t git remote add web ssh://user@host:%s" % bare_repo)
                _print("\n\t To push:")
                _print("\t\t git push web master")
                _print("")

            if arg.git_push_web:
                repo = arg.git_push_web
                cmd = "propel -w"
                _print("==== Setting WEB auto deploy on git push ...")
                git.update_post_receive_hook(repo, cmd)

            if arg.git_push_cmd:
                repo = arg.git_push_cmd[0]
                cmds = "; ".join(arg.git_push_cmd[1:])
                _print("==== Setting custom CMD on git push ...")
                git.update_post_receive_hook(repo, cmds)

            if arg.reload:
                _print("==== Refresh server ...")
                reload_server()
        _print("Completed!")
        _print("")

        if app:
            _print("")
            _print("=" * 80)
            _print("* PROPEL Deployment Summary *")
            _print("")
            if app.virtualenv.get("name"):
                _print("- Virtualenv: %s" % app.virtualenv.get("name"))
            if (arg.webs or arg.all_webs) and app.deployed_info:
                for i in app.deployed_info:
                    _print("- Webapp: %s" % i[0])
                    _print("\t Gunicorn port: %s" % i[1])
                    _print("\t Supervisor process name: %s" % i[2])

    except Exception as ex:
        if arg.debug:
            raise ex
        else:
            _print("")
            _print("*" * 80)
            _print("PROPEL ERROR: %s " % ex.__repr__())
            _print("*" * 80)

    _print("")


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def setup_propel():
    """
    To setup necessary paths and commands
    """
    global VERBOSE

    VERBOSE = True

    _print("Setting up Propel ... \n\n")

    MAINTENANCE_PAGE = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
    <title>Site Maintenance</title>
    <link href='//fonts.googleapis.com/css?family=Raleway:400,300,600' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    <style type="text/css">
      body { font: 20px "Raleway", Helvetica, sans-serif; color: #666; text-align: center; padding-top: 150px;}
        h1 { font-size: 50px; color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12 maintenance">
                <h1>We'll be back soon!</h1>
                <div>
                   Sorry for the inconvenience but we're performing some maintenance at the moment. <br>
                    We'll be back online shortly. <br>
                    Thanks!
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """

    _apt_get = get_dist_config("APT_GET")
    conf_file = "/etc/supervisord.conf"
    var_propel_dir = "/var/propel"
    maintenance_page = "%s/maintenance.html" % var_propel_dir

    if not os.path.isdir(SUPERVISOR_CONF_DIR):
        os.makedirs(SUPERVISOR_CONF_DIR)
    if not os.path.isdir(SUPERVISOR_LOG_DIR):
        os.makedirs(SUPERVISOR_LOG_DIR)
    if not os.path.isdir(var_propel_dir):
        os.makedirs(var_propel_dir)

    run("sudo %s -y update" % _apt_get)

    install_programs = get_dist_config("INSTALL_PROGRAMS")
    run("sudo %s -y install %s" % (_apt_get, " ".join(install_programs)))

    run("echo_supervisord_conf > %s" % conf_file)
    with open(conf_file, "a") as f:
        lines = "\n[include]\n"
        lines += "files = " + SUPERVISOR_CONF_DIR + "/*.conf\n"
        f.write(lines)

    # Add the virtualenvwrapper in bashrc
    run("mkdir -p ~/.virtualenvs")
    grep_test = 'if grep -q "#PROPEL-VIRTUALENVWRAPPER-START" ~/.bashrc; then echo "yes"; else echo "no"; fi'
    bash_venv = 'echo "\n#PROPEL-VIRTUALENVWRAPPER-START\n' \
                'export VIRTUALENVWRAPPER_PYTHON={PY_EXECUTABLE}\n' \
                'export WORKON_HOME=~/.virtualenvs\n' \
                'source /usr/local/bin/virtualenvwrapper.sh\n' \
                '#PROPEL-VIRTUALENVWRAPPER-END\n' \
                '" >> ~/.bashrc && source ~/.bashrc'.format(PY_EXECUTABLE=PY_EXECUTABLE)
    if run(grep_test, False) != "yes":
        run(bash_venv)

    upstart_cmd = get_dist_config("UPSTART_CMD")
    for s in get_dist_config("SERVICES"):
        run(upstart_cmd % s)
        run("sudo service %s start" % s)

    with open(maintenance_page, "wb") as f:
        f.write(MAINTENANCE_PAGE)

    print("\nPropel setup completed!")
