import StringIO
import logging
import os
import time

from tornado import gen
from tornado import testing
from tornado.testing import unittest
import mock
import rainbow_logging_handler
import requests

from kingpin import exceptions
from kingpin import utils
from kingpin.actors import misc


class TestUtils(unittest.TestCase):

    def test_str_to_class(self):
        class_string_name = 'tornado.testing.AsyncTestCase'
        returned_class = utils.str_to_class(class_string_name)
        self.assertEquals(testing.AsyncTestCase, returned_class)

        class_string_name = 'kingpin.actors.misc.Sleep'
        returned_class = utils.str_to_class(class_string_name)
        self.assertEquals(misc.Sleep, returned_class)

    def test_populate_with_env(self):
        tokens = {'UNIT_TEST': 'FOOBAR'}
        string = 'Unit %UNIT_TEST% Test'
        expect = 'Unit FOOBAR Test'
        result = utils.populate_with_tokens(string, tokens)
        self.assertEquals(result, expect)

    def test_populate_with_values_not_default(self):
        tokens = {'UNIT_TEST': 'FOOBAR', 'SECOND_UNIT': 'BARBAR'}
        string = 'Unit %UNIT_TEST|DEFAULT% Test %SECOND_UNIT|DEFAULT2%'
        expect = 'Unit FOOBAR Test BARBAR'
        result = utils.populate_with_tokens(string, tokens)
        self.assertEquals(result, expect)

    def test_populate_with_default(self):
        tokens = {'OTHER': 'TOKEN'}
        string = 'Unit %UNIT_TEST|DEFAULT% Test %SECOND_UNIT|1.2,3;4-5%'
        expect = 'Unit DEFAULT Test 1.2,3;4-5'
        result = utils.populate_with_tokens(string, tokens)
        self.assertEquals(result, expect)

    def test_populate_with_unicode_env(self):
        tokens = {'UNIT_TEST': u'FOOBAR'}
        string = 'Unit %UNIT_TEST% Test'
        expect = 'Unit FOOBAR Test'
        result = utils.populate_with_tokens(string, tokens)
        self.assertEquals(result, expect)

    def test_populate_with_bool(self):
        tokens = {'UNIT_TEST': True}
        string = 'Unit %UNIT_TEST% Test'
        expect = 'Unit True Test'
        result = utils.populate_with_tokens(string, tokens)
        self.assertEquals(result, expect)

    def test_populate_with_bogus_data_OK(self):
        tokens = {'UNIT_TEST': {'foobar': 'bat'}}
        string = 'Unit %UNIT_TEST% Test'
        expect = 'Unit %UNIT_TEST% Test'
        result = utils.populate_with_tokens(string, tokens, strict=False)
        self.assertEquals(result, expect)

    def test_populate_with_env_with_missing_variables(self):
        os.environ['UNIT_TEST'] = 'FOOBAR'
        string = 'Unit %UNIT_TEST% Test %NOTFOUNDVARIABLE%'
        with self.assertRaises(LookupError):
            utils.populate_with_tokens(string, os.environ)

    def test_populate_with_env_with_non_string_tokens(self):
        tokens = {'foo': False}
        string = 'Unit test'
        result = utils.populate_with_tokens(string, tokens)
        self.assertEquals(result, string)

    def test_populate_with_not_strict(self):
        tokens = {'UNIT_TEST': 'FOOBAR'}
        string = 'Unit {UNIT_TEST} {FAIL} Test'
        expect = 'Unit FOOBAR {FAIL} Test'
        result = utils.populate_with_tokens(
            string, tokens,
            left_wrapper='{', right_wrapper='}',
            strict=False)
        self.assertEquals(result, expect)

    def test_convert_script_to_dict(self):
        # Should work with string path to a file
        dirname, filename = os.path.split(os.path.abspath(__file__))
        examples = '%s/../../examples' % dirname
        simple = '%s/simple.json' % examples
        ret = utils.convert_script_to_dict(simple, {})
        self.assertEquals(type(ret), dict)

        # Should work with file instance also
        dirname, filename = os.path.split(os.path.abspath(__file__))
        examples = '%s/../../examples' % dirname
        simple = '%s/simple.json' % examples
        instance = open(simple)
        ret = utils.convert_script_to_dict(instance, {})
        self.assertEquals(type(ret), dict)

        # Should definitly support YAML as well
        dirname, filename = os.path.split(os.path.abspath(__file__))
        examples = '%s/../../examples' % dirname
        simple = '%s/simple.yaml' % examples
        instance = open(simple)
        ret = utils.convert_script_to_dict(instance, {})
        self.assertEquals(type(ret), dict)

    def test_convert_script_to_dict_bad_name(self):
        instance = StringIO.StringIO()  # Empty buffer will fail demjson.
        instance.__repr__ = lambda: 'Somefile.HAHA'

        with self.assertRaises(exceptions.InvalidScriptName):
            utils.convert_script_to_dict(instance, {})

    def test_convert_script_to_dict_junk(self):
        instance = StringIO.StringIO()
        instance.__repr__ = lambda: 'Somefile.json'

        with self.assertRaises(exceptions.InvalidScript):
            utils.convert_script_to_dict(instance, {})

        with self.assertRaises(exceptions.InvalidScript):
            utils.convert_script_to_dict('junk data', {})

        instance = StringIO.StringIO()
        instance.__repr__ = lambda: 'Somefile.yaml'
        instance.write('---bad-yaml')

        with self.assertRaises(exceptions.InvalidScript):
            utils.convert_script_to_dict(instance, {})

    def test_exception_logger(self):
        patch = mock.patch.object(utils.logging, 'getLogger')
        with patch as logger:
            reload(utils)

            @utils.exception_logger
            def raises_exc():
                raise Exception('Whoa')

            with self.assertRaises(Exception):
                raises_exc()

            self.assertEquals(1, logger().debug.call_count)
            logger().debug.assert_called_with(mock.ANY, exc_info=1)


class TestSetupRootLoggerUtils(unittest.TestCase):

    def setUp(self):
        utils.setup_root_logger()

    def test_setup_root_logger(self):
        # Since we're really checking if loggers get created properly,
        # make sure to wipe out any existing logging handlers on the Root
        # logger object.
        log = logging.getLogger()
        log.handlers = []

        # Default logger is basic
        logger = utils.setup_root_logger()
        self.assertEquals(type(logger.handlers[0]), logging.StreamHandler)
        self.assertEquals(logger.level, logging.WARNING)

    def test_setup_root_logger_color(self):
        # Since we're really checking if loggers get created properly,
        # make sure to wipe out any existing logging handlers on the Root
        # logger object.
        log = logging.getLogger()
        log.handlers = []

        # Color logger is nifty
        logger = utils.setup_root_logger(color=True)
        self.assertEquals(
            type(logger.handlers[0]),
            rainbow_logging_handler.RainbowLoggingHandler)
        self.assertEquals(logger.level, logging.WARNING)

    def test_setup_root_logger_with_level(self):
        # Since we're really checking if loggers get created properly,
        # make sure to wipe out any existing logging handlers on the Root
        # logger object.
        log = logging.getLogger()
        log.handlers = []

        logger = utils.setup_root_logger(level='debug')
        self.assertEquals(logger.level, logging.DEBUG)

    def test_setup_root_logger_with_syslog(self):
        # Since we're really checking if loggers get created properly,
        # make sure to wipe out any existing logging handlers on the Root
        # logger object.
        log = logging.getLogger()
        log.handlers = []

        logger = utils.setup_root_logger(syslog='local0')
        self.assertEquals(type(logger.handlers[0]),
                          logging.handlers.SysLogHandler)
        self.assertEquals(logger.handlers[0].facility, 'local0')

    def test_super_httplib_debug_logging(self):
        logger = utils.super_httplib_debug_logging()
        self.assertEquals(10, logger.level)

    def test_order_dict(self):
        d1 = {'foo': [1, 2, 3]}
        d2 = {'foo': [3, 2, 1]}

        ordered_d1 = utils.order_dict(d1)
        ordered_d2 = utils.order_dict(d2)

        self.assertEquals(ordered_d1, ordered_d2)


class TestCoroutineHelpers(testing.AsyncTestCase):

    @testing.gen_test
    def test_retry_with_backoff(self):

        # Define a method that will fail every time
        @gen.coroutine
        @utils.retry(excs=(requests.exceptions.HTTPError), retries=3)
        def raise_exception():
            raise requests.exceptions.HTTPError('Failed')

        with self.assertRaises(requests.exceptions.HTTPError):
            yield raise_exception()

        # Now a method that works
        @gen.coroutine
        @utils.retry(excs=(requests.exceptions.HTTPError), retries=3)
        def work():
            raise gen.Return(True)

        ret = yield work()
        self.assertEquals(ret, True)

    @testing.gen_test
    def testTornadoSleep(self):
        start = time.time()
        yield utils.tornado_sleep(0.1)
        stop = time.time()
        self.assertTrue(stop - start > 0.1)

    @testing.gen_test
    def test_repeating_log(self):
        logger = mock.Mock()  # used for tracking

        # Repeat this message 10 times per second
        # seconds=0 instructs Tornado to invoke this log on every IO loop
        # Below we yield gen.moment to allow IO loop iterations.
        # We do N+1 loops and check N count.
        logid = utils.create_repeating_log(logger.info, 'test', seconds=0)
        yield gen.moment
        yield gen.moment
        yield gen.moment
        yield gen.moment
        yield gen.moment

        utils.clear_repeating_log(logid)
        self.assertEquals(logger.info.call_count, 4)

        # Let's make sure that we don't keep looping our log message.
        yield gen.moment
        yield gen.moment
        self.assertEquals(logger.info.call_count, 4)

    @testing.gen_test
    def test_diff_dicts(self):
        p1 = {'a': 'a', 'b': 'b'}
        p2 = {'a': 'a', 'c': 'c'}

        self.assertEquals(None, utils.diff_dicts(p1, p1))
        self.assertNotEquals(None, utils.diff_dicts(p1, p2))
