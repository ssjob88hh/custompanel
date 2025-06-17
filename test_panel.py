import os
import panel


def setup_module(module):
    panel.app.config['TESTING'] = True
    panel.CONF_DIR = os.path.join(os.getcwd(), 'test_conf')
    panel.ENABLED_DIR = os.path.join(panel.CONF_DIR, 'enabled')
    os.makedirs(panel.CONF_DIR, exist_ok=True)
    os.makedirs(panel.ENABLED_DIR, exist_ok=True)


def teardown_module(module):
    import shutil
    shutil.rmtree(panel.CONF_DIR)


def test_add_and_remove():
    client = panel.app.test_client()
    resp = client.post('/add', data={'domain': 'example.com', 'root': '/var/www'})
    assert resp.status_code == 302
    assert os.path.exists(os.path.join(panel.CONF_DIR, 'example.com'))
    resp = client.get('/remove/example.com')
    assert resp.status_code == 302
    assert not os.path.exists(os.path.join(panel.CONF_DIR, 'example.com'))
