# -*- coding: utf-8 -*-


def Classification_File(category, file_path, write_path):
    count = 0
    with open(write_path, 'w', encoding='UTF-8') as w:
        with open(file_path, 'r', encoding='UTF-8') as f:
            for line in f.readlines():
                count += 1
                print("--------------------------------第%d篇：------------------------" % count)
                line = line.strip()
                if line.split('\t')[0] == category:
                    w.write(line + '\n')


if __name__ == "__main__":
    tmp_catalog = './data/cnews/'
    file_list = ['cnews.train.txt', 'cnews.test.txt', 'cnews.val.txt']
    # write_list = [tmp_catalog + 'train_token.txt', tmp_catalog + 'test_token.txt', tmp_catalog + 'val_token.txt']

    Category_list = ["体育", "娱乐", "家居", "房产", "教育", "时尚", "时政", "游戏", "科技", "财经"]
    for category in Category_list:
        print("=========================================开始处理《%s》类==================================================" % category)
        for i in range(len(file_list)):
            print("-------------------------------开始处理文本%s----------------------------------" % file_list[i])
            write_path = tmp_catalog + category + file_list[i]
            Classification_File(category, tmp_catalog+file_list[i], write_path)

    print("文本分类处理完成！")