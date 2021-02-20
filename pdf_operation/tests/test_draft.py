import pytest


from pdf_operation.constants import *
from pdf_operation.file_uitls import FolderOperation
from pdf_operation.identify_draft import IdentifyDraft

fo = FolderOperation(CASES_TRUE_DIR)
pdf_file_true_list = fo.fetch_specific_files()


@pytest.mark.parametrize('pdf_file_true', pdf_file_true_list)
def test_draft_file_true(pdf_file_true):
    """
    要不然一个个测试,或者分堆测试
    :param pdf_file:
    :return:
    """
    draft_id = IdentifyDraft(pdf_file_true, SEARCH_WORD)
    check_res = draft_id.search_draft_word()
    assert check_res == True


fo = FolderOperation(CASES_FALSE_DIR)
pdf_file_false_list = fo.fetch_specific_files()


@pytest.mark.parametrize('pdf_file_false', pdf_file_false_list)
def test_draft_file_false(pdf_file_false):
    """
    要不然一个个测试,或者分堆测试
    :param pdf_file:
    :return:
    """
    draft_id = IdentifyDraft(pdf_file_false, SEARCH_WORD)
    check_res = draft_id.search_draft_word()
    assert check_res == False

# if __name__ == '__main__':
#     print(sys.path)
