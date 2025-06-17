import os
import subprocess
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

CONF_DIR = os.environ.get('CONF_DIR', 'nginx_conf')
ENABLED_DIR = os.environ.get('ENABLED_DIR', os.path.join(CONF_DIR, 'enabled'))

os.makedirs(CONF_DIR, exist_ok=True)
os.makedirs(ENABLED_DIR, exist_ok=True)

SITE_TEMPLATE = """
server {
    listen 80;
    server_name {domain};
    root {root};
}
"""

INDEX_TEMPLATE = """
<!doctype html>
<html>
<head><title>Nginx Panel</title></head>
<body>
<h1>Nginx Panel</h1>
<h2>Sites</h2>
<ul>
{% for site in sites %}
<li>{{ site }} - <a href="{{ url_for('remove_site', name=site) }}">Remove</a></li>
{% endfor %}
</ul>
<h2>Add site</h2>
<form action="{{ url_for('add_site') }}" method="post">
Domain: <input type="text" name="domain">
Root: <input type="text" name="root">
<input type="submit" value="Add">
</form>
</body>
</html>
"""

@app.route('/')
def index():
    sites = sorted(os.listdir(CONF_DIR))
    return render_template_string(INDEX_TEMPLATE, sites=sites)

@app.route('/add', methods=['POST'])
def add_site():
    domain = request.form['domain']
    root = request.form['root']
    conf_path = os.path.join(CONF_DIR, domain)
    if os.path.exists(conf_path):
        return 'Site already exists', 400
    with open(conf_path, 'w') as f:
        f.write(SITE_TEMPLATE.format(domain=domain, root=root))
    symlink = os.path.join(ENABLED_DIR, domain)
    if not os.path.exists(symlink):
        os.symlink(conf_path, symlink)
    reload_nginx()
    return redirect(url_for('index'))

@app.route('/remove/<name>')
def remove_site(name):
    conf_path = os.path.join(CONF_DIR, name)
    symlink = os.path.join(ENABLED_DIR, name)
    if os.path.islink(symlink):
        os.unlink(symlink)
    if os.path.exists(conf_path):
        os.remove(conf_path)
    reload_nginx()
    return redirect(url_for('index'))

def reload_nginx():
    subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
