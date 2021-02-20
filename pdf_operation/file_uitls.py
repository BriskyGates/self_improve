import glob
import os


class FolderOperation():
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def fetch_specific_files(self, pattern="*.pdf"):
        file_list = glob.glob(os.path.join(self.folder_path, pattern))
        return file_list


if __name__ == '__main__':
    mypatg = r'C:\Users\Epiphony\Desktop\UTC2020年11月17日\cs01.dsv2020-11-17T142345SGNB004115150_gm 未提取_ONE\attachment'
    fo = FolderOperation(mypatg)
    # fo.fetch_identify_result()
    # temp = 'print data.pdf'
    # handle_same_filename(temp)
    # fo = FolderOperation(
    #     r'C:\Users\Epiphony\Desktop\海进_归类\HENKEL\详细文件\海进_2020年11月12日\alice.xin2020-11-12T114224转发 FWU20398\attachment')
    # fo.fetch_specific_xlsx()
    # PathDetails(r"C:\Users\Administrator\Desktop\海进_测试数据\Bill Of Lading - HAMA58351.PDF")
    # pd = FolderOperation(
    #     r"C:\Users\Administrator\Desktop\海进2020年11月11日_客户数据\alice.xin2020-11-11T141436U201089 S333\attachment")
    # pd.fetch_pdf_files()
