import unittest

from runtime_attestation import service_arguments


class ServiceEntrypoint(unittest.TestCase):
    def test_generated_tails_and_decoys(self):
        args = ['run', '--data-root', '/data', '--source-manifest', '/version/profile.json']
        prefix = 'def launch_admission(*args, **kwargs): pass\nlaunch_admission()\nfrom astrid_runtime.cli import main\n'
        legacy = prefix + 'sys.exit(main(' + repr(args) + '))'
        modern = (prefix + 'import inspect\n_args=' + repr(args) + '\n'
                  + "_context={'profile': '/version/profile.json', 'data_root': '/data'}\n"
                  + "sys.exit(main(_args, managed_launch=_context) if 'managed_launch' in inspect.signature(main).parameters else main(_args))")
        def parse(script):
            return service_arguments(['python', '-X', 'utf8', '-I', '-c', script])
        self.assertEqual(parse(legacy), args)
        self.assertEqual(parse(modern), args)
        for script in (legacy.replace('astrid_runtime.cli', 'unrelated.cli'),
                       modern.replace("'data_root': '/data'", "'data_root': '/other'"),
                       prefix + 'def decoy():\n    main(' + repr(args) + ')\n'):
            with self.subTest(script=script), self.assertRaisesRegex(ValueError, 'entrypoint'):
                parse(script)
