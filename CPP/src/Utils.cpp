#pragma warning(disable : 4996)

#include "../include/Utils.h"
#include "../include/main.h"
#include <io.h>
#include <fstream>

void Utils::Main(UtilsType type, string path, string fileType, string targetType) {
    this->path = path;
    this->fileType = fileType;
    this->targetType = targetType;
    files.clear();

    getAllFiles();
    

    if (type == UtilsType::RENAME) {
        renameFiles();
        return;
    }


    if (path.size() == 0) {
        switch (type) {
        case UtilsType::EPUB_TO_TXT:
            EPUB_TO_TXT::Main();
            break;
        case UtilsType::TXT_TO_TXT:
            TXT_TO_TXT::Main();
            break;
        case UtilsType::TXT_TO_TXT_DELETE_SPACE:
            TXT_TO_TXT_Delete_Space::Main();
            break;
        case UtilsType::LRC_TO_ASS:
            LRC_TO_ASS::Main();
            break;
        case UtilsType::SRT_TO_ASS:
            SRT_TO_ASS::Main();
            break;
        case UtilsType::NONE:
            break;
        default:
            break;
        }
    }
    else {
        for (auto file : files) {
            size_t pos = file.find_last_of(".");
            string name = file.substr(0, pos);
            string target = name + "." + targetType;

            switch (type) {
            case UtilsType::EPUB_TO_TXT:
                EPUB_TO_TXT::Main(file.c_str(), target.c_str());
                break;
            case UtilsType::TXT_TO_TXT:
                TXT_TO_TXT::Main(file.c_str(), target.c_str());
                break;
            case UtilsType::TXT_TO_TXT_DELETE_SPACE:
                TXT_TO_TXT_Delete_Space::Main(file.c_str(), target.c_str());
                break;
            case UtilsType::LRC_TO_ASS:
                LRC_TO_ASS::Main(file.c_str(), target.c_str());
                break;
            case UtilsType::SRT_TO_ASS:
                SRT_TO_ASS::Main(file.c_str(), target.c_str());
                break;
            case UtilsType::NONE:
                break;
            default:
                break;
            }
        }
    }
}

void Utils::getAllFiles() {
    // 文件句柄
    long long hFile = 0;
    // 文件信息
    struct _finddata_t fileinfo;

    string p;

    if ((hFile = _findfirst(p.assign(path).append("\\*" + fileType).c_str(), &fileinfo)) != -1) {
        do {
            // 保存文件的全路径
            files.push_back(p.assign(path).append("\\").append(fileinfo.name));

        } while (_findnext(hFile, &fileinfo) == 0);  // 寻找下一个，成功返回0，否则-1

        _findclose(hFile);
    }
}

void Utils::renameFiles() {
    if (files.size() == 0) {
        SetConsoleColor(ConsoleColor::White);
        printf("路径");
        SetConsoleColor(ConsoleColor::Red);
        printf(" %s ", path.c_str());
        SetConsoleColor(ConsoleColor::White);
        printf("下不存在后缀为");
        SetConsoleColor(ConsoleColor::Red);
        printf(" *.%s ", fileType.c_str());
        SetConsoleColor(ConsoleColor::White);
        printf("的文件, 请重新输入路径, 或退回到上一级重新输入文件后缀\n");
        return;
    }

    string prefix;
    SetConsoleColor(ConsoleColor::Yellow);
    printf("请输入文件前缀, null表示没有前缀:");
    SetConsoleColor(ConsoleColor::Red);
    cin >> prefix;
    SetConsoleColor(ConsoleColor::Clear);
    if (prefix == "null") prefix = "";


    int cnt = 0;
    SetConsoleColor(ConsoleColor::Yellow);
    printf("请输入起始cnt:");
    SetConsoleColor(ConsoleColor::Red);
    cin >> cnt;
    SetConsoleColor(ConsoleColor::Clear);

    for (auto file : files) {
        /* 重命名文件 */
        string command;
        // cnt: 000~999
        if(cnt < 10) command = "rename \"" + file + "\" " + prefix + "00" + to_string(cnt) + "." + targetType;
        else if(cnt < 100) command = "rename \"" + file + "\" " + prefix + "0" + to_string(cnt) + "." + targetType;
        else command = "rename \"" + file + "\" " + prefix + to_string(cnt) + "." + targetType;

        printf("command: %s\n", command.c_str());
        system(command.c_str());
        cnt++;
    }
    SetConsoleColor(ConsoleColor::White);
    printf("重命名完成, 共重命名 %d 个文件\n", files.size());
}
