import os

# Preload this much data in the bndl tool to determine input type of a stream
BNDL_PEEK_SIZE = 16384

# Defaults for creating bundles without specifying params
BNDL_DEFAULT_COMPATIBILITY_VERSION = '0'
BNDL_DEFAULT_DISK_SPACE = 1073741824
BNDL_DEFAULT_MEMORY = 402653184
BNDL_DEFAULT_NR_OF_CPUS = 0.1
BNDL_DEFAULT_ROLES = []
BNDL_DEFAULT_VERSION = '1'
BNDL_IGNORE_TAGS = ['latest']

CONDUCTR_SCHEME = 'CONDUCTR_SCHEME'

DEFAULT_SCHEME = os.getenv(CONDUCTR_SCHEME, 'http')
DEFAULT_PORT = os.getenv('CONDUCTR_PORT', '9005')
DEFAULT_SERVICE_LOCATOR_PORT = os.getenv('CONDUCTR_SERVICE_LOCATOR_PORT', '9008')
DEFAULT_BASE_PATH = os.getenv('CONDUCTR_BASE_PATH', '/')
DEFAULT_API_VERSION = os.getenv('CONDUCTR_API_VERSION', '2')
DEFAULT_DCOS_SERVICE = os.getenv('CONDUCTR_DCOS_SERVICE', 'conductr')
DEFAULT_CLI_SETTINGS_DIR = os.getenv('CONDUCTR_CLI_SETTINGS_DIR', '{}/.conductr'.format(os.path.expanduser('~')))
DEFAULT_RESOLVE_CACHE_DIR = '{}/cache'.format(DEFAULT_CLI_SETTINGS_DIR)
DEFAULT_CLI_TMP_DIR = os.path.abspath(os.getenv('CONDUCTR_CLI_TMP_DIR', '{}/tmp'.format(DEFAULT_CLI_SETTINGS_DIR)))
DEFAULT_BUNDLE_RESOLVE_CACHE_DIR = os.getenv('CONDUCTR_BUNDLE_RESOLVE_CACHE_DIR',
                                             '{}/bundle'.format(DEFAULT_RESOLVE_CACHE_DIR))
DEFAULT_CONFIGURATION_RESOLVE_CACHE_DIR = os.getenv('CONDUCTR_CONFIGURATION_RESOLVE_CACHE_DIR',
                                                    '{}/configuration'
                                                    .format(DEFAULT_RESOLVE_CACHE_DIR))
DEFAULT_CUSTOM_SETTINGS_FILE = os.getenv('CONDUCTR_CUSTOM_SETTINGS_FILE',
                                         '{}/settings.conf'.format(DEFAULT_CLI_SETTINGS_DIR))
DEFAULT_CUSTOM_PLUGINS_DIR = os.getenv('CONDUCTR_CUSTOM_PLUGINS_DIR',
                                       '{}/plugins'.format(DEFAULT_CLI_SETTINGS_DIR))
DEFAULT_OFFLINE_MODE = os.getenv('CONDUCTR_OFFLINE_MODE', False)
DEFAULT_SANDBOX_IMAGE_DIR = os.path.abspath(os.getenv('CONDUCTR_SANDBOX_IMAGE_DIR',
                                                      '{}/images'.format(DEFAULT_CLI_SETTINGS_DIR)))
DEFAULT_SANDBOX_TMP_DIR = os.path.abspath(os.getenv('CONDUCTR_SANDBOX_TMP_DIR',
                                                    '{}/tmp'.format(DEFAULT_SANDBOX_IMAGE_DIR)))
DEFAULT_SANDBOX_ADDR_RANGE = os.getenv('CONDUCTR_SANDBOX_ADDR_RANGE', '192.168.10.0/24')
DEFAULT_SANDBOX_PROXY_DIR = os.path.abspath(os.getenv('CONDUCTR_SANDBOX_PROXY_DIR',
                                                      '{}/proxy'.format(DEFAULT_CLI_SETTINGS_DIR)))
# Prefixed with `sandbox-` to avoid overlap with `cond-` ConductR container names, causing the proxy to be stopped
# when sandbox stop is called for docker containers.
DEFAULT_SANDBOX_PROXY_CONTAINER_NAME = os.getenv('CONDUCTR_SANDBOX_PROXY_CONTAINER_NAME', 'sandbox-haproxy')
DEFAULT_ERROR_LOG_FILE = os.path.abspath(os.getenv('CONDUCTR_CLI_ERROR_LOG',
                                                   '{}/errors.log'.format(DEFAULT_CLI_SETTINGS_DIR)))
DEFAULT_LICENSE_DOWNLOAD_URL = os.getenv('CONDUCTR_LICENSE_DOWNLOAD_URL',
                                         'https://www.lightbend.com/product/conductr/license')
DEFAULT_LICENSE_FILE = os.path.abspath(os.getenv('CONDUCTR_LICENSE_FILE',
                                                 '{}/.lightbend/license'.format(os.path.expanduser('~'))))
DEFAULT_AUTH_TOKEN_FILE = os.path.abspath(os.getenv('CONDUCTR_AUTH_TOKEN_FILE',
                                                    '{}/.lightbend/auth-token'.format(os.path.expanduser('~'))))
DEFAULT_WAIT_TIMEOUT = 60  # seconds

# Must be able to hold the digest value, name of algorithm, and newline character
DIGEST_TRAIL_SIZE = 100

FEATURE_PROVIDE_PROXYING = 'proxying'

FEATURE_PROVIDE_LOGGING = 'logging'

# When reading and writing to IO devices, buffer this many bytes at a time
IO_CHUNK_SIZE = 32768
