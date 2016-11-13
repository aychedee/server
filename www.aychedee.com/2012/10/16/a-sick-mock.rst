public: yes
tags: [mocking, Python, learning]
summary: |
  Down a mocking rabbit hole.

A sick mock
===========

You can mock too much sometimes...

.. code-block:: python

    class ParseReportTest(unittest.TestCase):

         @patch('__builtin__.open')
         def test_get_report_string(self, mock_open):

             mock_file, mock_context_manager = Mock(), Mock()
             mock_enter, mock_exit = Mock(), Mock()
             mock_open.return_value = mock_context_manager
             mock_file.read.return_value = sentinel.file_contents
             mock_enter.return_value = mock_file
             setattr(mock_context_manager, '__enter__', mock_enter)
             setattr(mock_context_manager, '__exit__', mock_exit)

             quota_report = get_report_string()

             self.assertEqual(quota_report, sentinel.file_contents)
             self.assertEqual(mock_open.call_args_list, [call('/srv/report')])


I thought this was pretty interesting. It is the first time I have tried to
mock a built in context manager. In some situations would probably be the only
solution. But in this instance mocking a constant made more sense. So I ended
up replacing it with:

.. code-block:: python

        @patch('anywhere.files.management.commands.warn_about_quotas.QUOTA_REPORT_LOCATION')
        def test_get_report_string(self, mock_location):

            fh, temp_report_path = mkstemp()
            mock_location = temp_report_path
            fh.write(QUOTA_TEST_DATA)

            quota_report = get_report_string()

            self.assertEqual(quota_report, QUOTA_TEST_DATA)

            os.remove(temp_report_path)

Anyway, it was still interesting to learn how to mock a built in context
manager. Figuring out how to refer to the right object was worth it all
by itself.
