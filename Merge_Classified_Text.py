# -*- coding: utf-8 -*-


def Merge_Text(write_path, file_list):
    with open(write_path, 'w', encoding='UTF-8') as w:
        for i in range(len(file_list)):
            with open(file_list[i], 'r', encoding='UTF-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    w.write(line + '\n')


if __name__ == "__main__":
    tmp_catalog = './data/token/'
    write_catalog = './data/merge_token/'

    Category_list = ["体育", "娱乐", "家居", "房产", "教育", "时尚", "时政", "游戏", "科技", "财经"]
    token_post_list = ['_train_token.txt', '_test_token.txt', '_val_token.txt']

    train_file_list = [tmp_catalog + category + token_post_list[0] for category in Category_list]
    test_file_list = [tmp_catalog + category + token_post_list[1] for category in Category_list]
    val_file_list = [tmp_catalog + category + token_post_list[2] for category in Category_list]

    print("train_file_list", train_file_list)
    print("test_file_list", test_file_list)
    print("val_file_list", val_file_list)

    file_list = [train_file_list, test_file_list, val_file_list]

    write_list = [write_catalog+"train_token.txt", write_catalog+"test_token.txt", write_catalog+"val_token.txt"]

    for i in range(len(write_list)):
        print( "=========================================开始处理《%s》文本==================================================" % write_list[i])
        Merge_Text(write_list[i], file_list[i])
        print("《%s》文本合并完成！-------------------" % write_list[i])

    print("文本合并处理完成！")