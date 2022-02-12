import zipfile

from selenium import webdriver
from articles.models import PublishedPost


def get_params(instance_id):
    post = PublishedPost.objects.get(id=instance_id)
    PROXY_HOST = post.proxy.ip
    PROXY_PORT = post.proxy.port
    PROXY_USER = post.proxy.login
    PROXY_PASS = post.proxy.password

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
    
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    return manifest_json, background_js


def get_chromedriver(instance_id, use_proxy=False, user_agent=None):
    params = get_params(instance_id)
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", params[0])
            zp.writestr("background.js", params[1])
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def get_chromedriver_remote(instance_id, use_proxy=False, user_agent=None):
    capabilities = {
        "browserName": "chrome",
        "version": "78.0",
        "platform": "LINUX"
    }

    params = get_params(instance_id)
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", params[0])
            zp.writestr("background.js", params[1])
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Remote(
        command_executor='http://localhost:444',
        desired_capabilities=capabilities,
        options=chrome_options
    )
    return driver
