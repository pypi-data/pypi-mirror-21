from pyaxmlparser.arscparser import ARSCParser
from pyaxmlparser.axmlprinter import AXMLPrinter
from pyaxmlparser.utils import get_zip_file


class APK:

    NS_ANDROID_URI = 'http://schemas.android.com/apk/res/android'

    def __init__(self, apk):
        self.apk = apk
        self.zip_file = get_zip_file(apk)
        self.validate()
        self.axml = AXMLPrinter(self.zip_file.read('AndroidManifest.xml'))
        self.xml = self.axml.get_xml_obj()
        self.arsc = ARSCParser(self.zip_file.read('resources.arsc'))

    def validate(self):
        zip_files = set(self.zip_file.namelist())
        required_files = {'AndroidManifest.xml', 'resources.arsc'}
        assert required_files.issubset(zip_files)

    @property
    def application(self):
        app_name_hex = self.xml.getElementsByTagName("application")[0].getAttribute("android:label")
        if app_name_hex.startswith('@'):
            _pkg_name = self.arsc.get_packages_names()[0]
            rsc = self.get_resource(app_name_hex, _pkg_name)
            if rsc:
                app_name = rsc
        else:
            app_name = self.package
        return app_name

    @property
    def version_name(self):
        version_name = self.xml.documentElement.getAttributeNS(self.NS_ANDROID_URI, "versionName")
        if version_name.startswith("@"):
            rsc = self.get_resource(version_name, self.package)
            if rsc:
                version_name = rsc

        if not version_name:
            version_name = self.xml.documentElement.getAttribute("android:versionName")
        return version_name

    def get_resource(self, key, value):
        try:
            key = '0x' + key[1:]
            hex_value = self.arsc.get_id(value, int(key, 0))[1]
            rsc = self.arsc.get_string(value, hex_value)[1]
        except:
            rsc = None
        return rsc

    @property
    def version_code(self):
        version_code = self.xml.documentElement.getAttributeNS(self.NS_ANDROID_URI, "versionCode")
        if not version_code:
            version_code = self.xml.documentElement.getAttribute("android:versionCode")
        return version_code

    @property
    def package(self):
        return self.xml.documentElement.getAttribute("package")

    @property
    def icon_info(self):
        icon_hex = '0x' + self.xml.getElementsByTagName('application')[0].getAttribute('android:icon')[1:]
        icon_data = self.arsc.get_id(self.package, int(icon_hex, 0))
        icon_type, icon_name = icon_data[0], icon_data[1]
        return icon_type, icon_name

    @property
    def icon_data(self):
        icon_type, icon_name = self.icon_info

        if not icon_name:
            return

        if icon_type and 'mipmap' in icon_type:
            search_path = 'res/mipmap'
        else:
            search_path = 'res/drawable'

        for filename in self.zip_file.namelist():
            if filename.startswith(search_path):
                if icon_name in filename.split('/')[-1].rsplit('.', 1):
                    icon_data = self.zip_file.read(filename)
                    return icon_data
