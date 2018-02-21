from unittest import mock

from company.tasks import import_ch_companies, lock_acquired


@mock.patch('company.tasks.lock_acquired', mock.Mock(return_value=True))
@mock.patch('company.tasks.call_command')
def test_task_import_ch_companies(mocked_call_command):
    import_ch_companies()
    mocked_call_command.assert_called_once_with('import_ch_companies')


@mock.patch('company.tasks.cache')
def test_lock_acquired(mocked_cache):
    lock_acquired('foobar')
    mocked_cache.add.assert_called_once_with('foobar', 'acquired', 72000)
