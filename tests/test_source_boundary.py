import pathlib, xml.etree.ElementTree as ET, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Scope(unittest.TestCase):
    def test_manifest_no_permissions(self):
        tree=ET.parse(ROOT/'app/src/main/AndroidManifest.xml')
        self.assertFalse(any(e.tag.endswith('uses-permission') for e in tree.iter()))
    def test_no_services_receivers(self):
        tree=ET.parse(ROOT/'app/src/main/AndroidManifest.xml')
        self.assertFalse(any(e.tag in ('service','receiver','provider') for e in tree.iter()))
    def test_no_network_or_minecraft_calls_in_compiled_java(self):
        sources=list((ROOT/'app/src/main/java').rglob('*.java'))
        self.assertEqual(len(sources),3)
        for p in sources:
            content=p.read_text()
            for forbidden in ('import java.net.', 'import java.io.', 'import android.net.', 'WebSocketProbeServer', 'MinecraftServer', 'Runtime.getRuntime(', 'ProcessBuilder(', 'startForegroundService(', 'getExternalFilesDir(', 'android.permission.INTERNET'):
                self.assertNotIn(forbidden,content,p.name)
    def test_readme_marks_install_not_authorized(self):
        self.assertIn('NOT authorized', (ROOT/'README.md').read_text())
if __name__=='__main__': unittest.main()
