import os
gettext = lambda s: s

PROJECT_ROOT = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '..')

def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)

BASE_URL = 'http://pycon.local.python.org.uy:8000'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sophilabs', 'contact@sophilabs.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = rel('media')
MEDIA_URL = '/media/'
STATIC_ROOT = rel('collectedstatic')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    rel('static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
PIPELINE = False


SECRET_KEY = 'zq($m9-l453vuha7wn(0p_xq38xb&amp;6a15^=3ix--#wu(zq)_u5'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware',
)

OFFSITE_URLS = ['/2012']

ROOT_URLCONF = 'pyconuy.urls'
WSGI_APPLICATION = 'pyconuy.wsgi.application'

TEMPLATE_DIRS = (
    rel('templates'),
    rel('main/templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
    'django.contrib.messages.context_processors.messages',
    'main.context_processors.add_site_config',
    'main.context_processors.add_settings',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    #pinax
    'pinax.apps.account',
    'emailconfirmation',

    #cms
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'cmsplugin_blog',
    'simple_translation',
    'tagging',
    'cms.plugins.file',
    #'cms.plugins.flash',
    #'cms.plugins.googlemap',
    'cms.plugins.link',
    'cms.plugins.picture',
    #'cms.plugins.teaser',
    'cms.plugins.text',
    #'cms.plugins.video',
    #'cms.plugins.twitter',
    'djangocms_utils',
    'missing',

    #others
    'bootstrap',
    'south',

    'main',
    'conference',
    'background',
    'common',
    'account',
)

APPEND_SLASH = False
CMS_TEMPLATES = (
    ('base.html', 'Base'),
)

LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)

ACCEPTING_PROPOSALS = True
MARKITUP_AUTO_PREVIEW = True
MARKITUP_SET = "markitup/sets/markdown-custom"
MARKITUP_SKIN = "markitup/skins/simple"
MARKITUP_FILTER = ["markdown.markdown", {}]
MARKITUP_MEDIA_URL = STATIC_URL

JQUERY_JS = '/static/jquery/js/jquery.js'
JQUERY_UI_JS = '/static/jquery/js/jquery-ui.js'
JQUERY_UI_CSS = '/static/jquery/css/jquery-ui.css'
CMSPLUGIN_BLOG_PLACEHOLDERS = ('text', 'excerpt',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PROPOSALS_SEND_TO = ['speakers@python.org.uy']

SHOW_VIDEOS_OPTION = False

LOGIN_URL = '/sign'
LOGOUT_URL = '/sign-out'
LOGIN_REDIRECT_URL = '/profile'
LOGIN_ERROR_URL = '/'

try:
    from settings_local import *
except ImportError:
    pass

LOCALE_PATHS = ( rel('conf/locale/'),)
